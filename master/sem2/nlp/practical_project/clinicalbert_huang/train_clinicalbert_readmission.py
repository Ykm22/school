import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, precision_recall_curve
from tqdm import tqdm
import os
import gc # Garbage collector

# --- Configuration ---
PROCESSED_DATA_PATH = './processed_readmission_data.parquet'
MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT" # Or other clinical BERT variant
OUTPUT_DIR = "./trained_models_and_results/"
MAX_SEQ_LENGTH = 512 # As per paper's BERT usage
BATCH_SIZE = 8 # Paper uses 56, adjust based on your GPU memory. Start small.
ACCUMULATION_STEPS = 7
LEARNING_RATE = 2e-5
EPOCHS = 3 # Paper uses 3 with early stopping
N_SPLITS = 5 # 5-fold cross-validation
PATIENCE_EARLY_STOPPING = 1 # Number of epochs with no improvement to wait before stopping
AGGREGATION_C = 2.0 # Constant c for Eq. 4

os.makedirs(OUTPUT_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# --- Dataset Class ---
class MimicReadmissionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False, # ClinicalBERT might not use token_type_ids if not pre-trained with NSP format
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.float)
        }

# --- Model Definition (ClinicalBERT + Classifier Head) ---
class ClinicalBertForReadmission(nn.Module):
    def __init__(self, model_name):
        super(ClinicalBertForReadmission, self).__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        # Classifier head as per Appendix A: 768 -> 2048 -> 768 -> 1
        self.classifier = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, 2048),
            nn.ReLU(),
            # nn.Dropout(0.1), # Optional dropout
            nn.Linear(2048, 768),
            nn.ReLU(),
            # nn.Dropout(0.1), # Optional dropout
            nn.Linear(768, 1) # Output for binary classification (logits)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        # Use the [CLS] token's representation for classification
        pooled_output = outputs.pooler_output # Some models might provide this directly
        # Or, more commonly for BERT classification tasks if pooler_output is not ideal:
        # cls_output = outputs.last_hidden_state[:, 0, :] # [batch_size, hidden_size]
        
        # The paper's h[CLS] refers to the output corresponding to the [CLS] token.
        # For many HuggingFace BERT models, outputs.last_hidden_state[:, 0] is this.
        # Using pooler_output is also common, typically it's the [CLS] token's output passed through a Linear layer and Tanh.
        # Let's stick to pooler_output if available and standard. If issues, switch to last_hidden_state[:,0,:].
        if pooled_output is None:
             pooled_output = outputs.last_hidden_state[:, 0]

        logits = self.classifier(pooled_output)
        return logits

# --- Helper function to calculate RP80 ---
def calculate_rp80(y_true, y_scores):
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    rp80_recall = 0.0
    # Find recall at the first point where precision is >= 0.8
    # Iterate backwards on precision/recall arrays as thresholds are typically increasing for y_scores
    for i in range(len(precision) - 1, -1, -1): # Start from the end (higher thresholds)
        if precision[i] >= 0.80:
            rp80_recall = recall[i] # Take the recall at this point
            break 
            # If you want the max recall for any P >= 0.8:
            # if precision[i] >= 0.80:
            #    rp80_recall = max(rp80_recall, recall[i])
    return rp80_recall


def train_epoch(model, data_loader, loss_fn, optimizer, device, scheduler, n_examples, accumulation_steps): # Added accumulation_steps
    model.train()
    losses = []
    # correct_predictions = 0 # Accuracy calculation removed for brevity, can be added back
    
    optimizer.zero_grad() # Zero gradients at the beginning of the epoch

    for batch_idx, d in enumerate(tqdm(data_loader, desc="Training")):
        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        labels = d["labels"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = loss_fn(outputs.squeeze(-1), labels) # Squeeze for BCEWithLogitsLoss
        
        # Normalize loss to account for accumulation
        loss = loss / accumulation_steps 
        losses.append(loss.item() * accumulation_steps) # Store the original-scale loss

        loss.backward()

        if (batch_idx + 1) % accumulation_steps == 0:
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # Gradient clipping
            optimizer.step()
            scheduler.step() # Step scheduler when optimizer steps
            optimizer.zero_grad() # Zero gradients after optimizer step
        
        # Log progress (optional, adjust frequency)
        if batch_idx % 100 == 0: 
            # Calculate average loss so far from the scaled down losses
            current_avg_loss = np.mean(losses) if losses else 0
            print(f"  Batch {batch_idx}/{len(data_loader)}, Current Avg Loss: {current_avg_loss:.4f}")

    # Handle any remaining gradients if the total number of batches is not a multiple of accumulation_steps
    # This part is often skipped for simplicity, but for completeness:
    # if len(data_loader) % accumulation_steps != 0:
    #     nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    #     optimizer.step()
    #     scheduler.step()
    #     optimizer.zero_grad()

    return np.mean(losses)


# --- Evaluation Function ---
# This eval function processes subsequences individually. Aggregation per patient is done after.
def eval_model_on_subsequences(model, data_loader, loss_fn, device, n_examples):
    model.eval()
    losses = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for d in tqdm(data_loader, desc="Evaluating"):
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            labels = d["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs.squeeze(-1), labels)
            
            probs = torch.sigmoid(outputs).squeeze(-1)

            losses.append(loss.item())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
    return np.mean(losses), np.array(all_labels), np.array(all_probs)


# --- Main Script ---
print("Loading preprocessed data...")
df = pd.read_parquet(PROCESSED_DATA_PATH)
# For demonstration, let's sample if the dataset is too large for quick tests
# df = df.sample(n=1000, random_state=42).reset_index(drop=True) # Comment out for full run

# The paper's strategy of splitting one note into multiple subsequences if it's too long
# is handled by the tokenizer's `truncation=True` and `max_length=MAX_SEQ_LENGTH`.
# For a single patient, if their concatenated notes exceed MAX_SEQ_LENGTH,
# the current MimicReadmissionDataset takes only the first MAX_SEQ_LENGTH tokens.
# To implement Equation 4 properly, we need to:
# 1. Split long texts into multiple chunks OF MAX_SEQ_LENGTH.
# 2. Get predictions for each chunk.
# 3. Aggregate these predictions per patient using Equation 4.

# Let's refine data preparation for Equation 4:
# We need to associate subsequences with their original HADM_ID
all_subsequences = []
all_subsequence_labels = []
all_subsequence_hadm_ids = []
tokenizer_for_splitting = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Splitting notes into subsequences for BERT and Equation 4...")
for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Chunking notes"):
    text = str(row['text'])
    label = row['label']
    hadm_id = row['HADM_ID']

    # Tokenize the entire text to see how many chunks it would make
    # We are not padding here, just getting input_ids to count chunks
    tokenized_full_text = tokenizer_for_splitting(text, add_special_tokens=True, return_attention_mask=False)['input_ids']
    
    num_tokens = len(tokenized_full_text)
    # Effective max length for content tokens is MAX_SEQ_LENGTH - 2 (for [CLS] and [SEP])
    # However, tokenizer handles this with add_special_tokens=True.
    # We pass the text directly to the dataset, which then tokenizes with truncation.
    # For Eq. 4, we need to manually create these chunks.
    
    # If the text is short enough, it's one subsequence
    if num_tokens <= MAX_SEQ_LENGTH:
        all_subsequences.append(text)
        all_subsequence_labels.append(label)
        all_subsequence_hadm_ids.append(hadm_id)
    else:
        # Create overlapping chunks as often done, or simple consecutive chunks
        # For simplicity, let's do consecutive chunks.
        # The tokenizer handles adding [CLS] and [SEP] to each chunk.
        # We need to feed the raw text chunks to the tokenizer.
        
        # This is a simplified chunking. A more robust way uses tokenizer's stride.
        # For now, let's just pass the full text and rely on MimicReadmissionDataset's truncation
        # for training, and implement a special eval that handles chunking.
        # This means training happens on the first MAX_SEQ_LENGTH of each note.
        # For evaluation faithful to Eq 4, we'd need to process all chunks of a note.

        # For a simpler setup aligning with typical BERT fine-tuning on truncated text:
        # We train on potentially truncated texts.
        # For evaluation, if we want to use Eq 4, the eval loop must internally chunk.
        # The current eval_model_on_subsequences evaluates on these (potentially truncated) texts.
        # Let's proceed with this simpler setup first and note Eq4 as an advanced eval step.
        
        # Simpler approach: each row in `df` is one training/eval sample (potentially truncated)
        # Eq4 would require grouping predictions by HADM_ID later.
        pass # Data is already one row per HADM_ID, text will be truncated by Dataset

X = df['text'].tolist()
y = df['label'].tolist()
hadm_ids_list = df['HADM_ID'].tolist() # Keep track of HADM_ID for Eq4 style evaluation

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)
fold_results = []
all_epoch_logs = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    print(f"\n--- Fold {fold+1}/{N_SPLITS} ---")

    train_texts = [X[i] for i in train_idx]
    train_labels = [y[i] for i in train_idx]
    # train_hadm_ids = [hadm_ids_list[i] for i in train_idx] # Not directly used in this simpler training

    val_texts = [X[i] for i in val_idx]
    val_labels = [y[i] for i in val_idx]
    val_hadm_ids = [hadm_ids_list[i] for i in val_idx] # Used for Eq4 style eval

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    train_dataset = MimicReadmissionDataset(train_texts, train_labels, tokenizer, MAX_SEQ_LENGTH)
    val_dataset = MimicReadmissionDataset(val_texts, val_labels, tokenizer, MAX_SEQ_LENGTH)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    model = ClinicalBertForReadmission(MODEL_NAME).to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE) # Paper uses Adam, AdamW is common for BERT
    total_steps = len(train_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps) # Paper doesn't specify warmup
    loss_fn = nn.BCEWithLogitsLoss().to(device)

    best_val_loss = float('inf')
    epochs_no_improve = 0
    # current_fold_epoch_logs = []

    for epoch in range(EPOCHS):
        print(f"Epoch {epoch+1}/{EPOCHS}")
        train_loss = train_epoch(model, train_loader, loss_fn, optimizer, device, scheduler, len(train_dataset), 
                                 ACCUMULATION_STEPS
        )
        print(f"Training Loss: {train_loss:.4f}")

        val_loss, val_raw_labels, val_raw_probs = eval_model_on_subsequences(model, val_loader, loss_fn, device, len(val_dataset))
        print(f"Validation Loss: {val_loss:.4f}")
        all_epoch_logs.append({ # <--- ADD THIS
            'fold': fold + 1,
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'val_loss': val_loss
        })
        # current_fold_epoch_logs.append({'epoch': epoch + 1, ...}) # Optional

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), os.path.join(OUTPUT_DIR, f'clinicalbert_fold{fold+1}_best.bin'))
            epochs_no_improve = 0
            print("Validation loss improved. Saved model.")
        else:
            epochs_no_improve += 1
            print(f"Validation loss did not improve for {epochs_no_improve} epoch(s).")

        if epochs_no_improve >= PATIENCE_EARLY_STOPPING:
            print(f"Early stopping triggered after {epoch+1} epochs.")
            break
    
    # Load best model for this fold for final evaluation
    print("Loading best model for evaluation on validation set...")
    model.load_state_dict(torch.load(os.path.join(OUTPUT_DIR, f'clinicalbert_fold{fold+1}_best.bin')))
    
    # --- Evaluation with Equation 4 ---
    # This requires re-evaluating or structuring storage to group by HADM_ID
    # For each HADM_ID in validation set, get all its (potentially truncated) notes/subsequences
    # This is simplified: Assuming one main note per HADM_ID, potentially truncated.
    # To truly implement Eq4 as in paper, if a *single* patient's notes are very long and
    # manually chunked into multiple inputs for BERT:
    
    # Step 1: Group raw predictions by HADM_ID from val_loader.
    # val_loader processes each item from val_dataset. If val_dataset has one entry per HADM_ID
    # (even if text is truncated), then val_raw_probs and val_hadm_ids are aligned.
    
    # If each HADM_ID can have MULTIPLE rows in val_dataset (due to manual chunking *before* Dataset creation)
    # then we need to aggregate. For now, assume val_dataset has unique HADM_IDs.
    
    patient_predictions = {} # key: hadm_id, value: list of probabilities for its subsequences
    # This loop simulates getting predictions for each subsequence of each patient
    # In our current val_dataset, each item is one patient (potentially truncated note)
    # So, each patient has only one "subsequence" probability from val_raw_probs directly.
    
    # To make Eq4 work as intended if a single note was split into N BERT inputs:
    # You would need to modify eval_model_on_subsequences to take a list of texts for one patient,
    # process each text chunk, get a prob, and then apply Eq4.
    # Or, easier: run inference on all chunks of all val patients, store (hadm_id, chunk_prob).
    # Then aggregate.

    # For this script, we'll apply Eq.4 in a simplified way:
    # If a patient's note was long enough to be split into N subsequences (manually),
    # we'd have N probabilities. Here, each patient has one prob (from one, possibly truncated, note).
    # So N=1 for each patient. Eq.4 simplifies.
    # (P_max + P_mean * 1/c) / (1 + 1/c) = (P + P * 1/c) / (1 + 1/c) = P * (1 + 1/c) / (1 + 1/c) = P.
    # So, for N=1, Eq.4 gives back the original probability.
    # The paper's Eq.4 makes sense when a patient has *multiple note entries* that are processed,
    # or one *very long note* is split into multiple BERT inputs.
    
    # Let's demonstrate the structure if we had multiple subsequence probabilities per patient:
    # `val_patient_probs` would be a dictionary: {hadm_id1: [prob1_1, prob1_2], hadm_id2: [prob2_1], ...}
    # `val_patient_true_labels` would be: {hadm_id1: label1, hadm_id2: label2, ...}
    
    # Current output `val_raw_probs` and `val_hadm_ids` gives one prob per HADM_ID
    # So, essentially, n=1 for all patients in this simplified setup.
    final_patient_probs = []
    final_patient_labels = []
    
    # Create a temporary DataFrame to map HADM_ID to its single probability and true label
    temp_eval_df = pd.DataFrame({
        'HADM_ID': val_hadm_ids, # From the val_idx split earlier
        'PROB': val_raw_probs,   # Probabilities from eval_model_on_subsequences
        'LABEL': val_raw_labels  # True labels
    })
    
    # In this simplified case (n=1), Eq. 4 becomes P_final = P_subsequence.
    # If you had multiple subsequences per patient, you'd group by HADM_ID and apply Eq. 4:
    # Example for true Eq. 4 application (if you had multiple probs per HADM_ID):
    # for hadm_id, group in temp_eval_df.groupby('HADM_ID'):
    #     probs_for_patient = group['PROB'].tolist()
    #     true_label = group['LABEL'].iloc[0] # Assuming label is same for all subsequences of a patient
    #     n = len(probs_for_patient)
    #     if n == 0: continue
    #     p_max = np.max(probs_for_patient)
    #     p_mean = np.mean(probs_for_patient)
    #     
    #     final_prob = (p_max + p_mean * (n / AGGREGATION_C)) / (1 + (n / AGGREGATION_C))
    #     final_patient_probs.append(final_prob)
    #     final_patient_labels.append(true_label)
    
    # Since current setup has n=1 for each patient entry in val_dataset:
    final_patient_probs = temp_eval_df['PROB'].tolist()
    final_patient_labels = temp_eval_df['LABEL'].tolist()

    # Calculate metrics on these (potentially aggregated) patient-level predictions
    auroc = roc_auc_score(final_patient_labels, final_patient_probs)
    auprc = average_precision_score(final_patient_labels, final_patient_probs)
    rp80 = calculate_rp80(final_patient_labels, final_patient_probs)

    print(f"Fold {fold+1} Validation AUROC: {auroc:.4f}")
    print(f"Fold {fold+1} Validation AUPRC: {auprc:.4f}")
    print(f"Fold {fold+1} Validation RP80: {rp80:.4f}")
    
    fold_results.append({'fold': fold+1, 'auroc': auroc, 'auprc': auprc, 'rp80': rp80, 'val_loss': best_val_loss})
    
    del model, train_loader, val_loader, train_dataset, val_dataset, optimizer, scheduler
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

print("\n--- Cross-Validation Results ---")
results_df = pd.DataFrame(fold_results)
print(results_df)
print("\nAverage Metrics:")
print(f"  AUROC: {results_df['auroc'].mean():.4f} +/- {results_df['auroc'].std():.4f}")
print(f"  AUPRC: {results_df['auprc'].mean():.4f} +/- {results_df['auprc'].std():.4f}")
print(f"  RP80:  {results_df['rp80'].mean():.4f} +/- {results_df['rp80'].std():.4f}")

results_df.to_csv(os.path.join(OUTPUT_DIR, "cv_results.csv"), index=False)
print(f"Results saved to {os.path.join(OUTPUT_DIR, 'cv_results.csv')}")

# Save the detailed epoch-level logs
epoch_logs_df = pd.DataFrame(all_epoch_logs) # <--- ADD THIS
epoch_logs_df.to_csv(os.path.join(OUTPUT_DIR, "epoch_level_logs.csv"), index=False) # <--- ADD THIS
print(f"Detailed epoch-level logs saved to {os.path.join(OUTPUT_DIR, 'epoch_level_logs.csv')}") # <--- ADD THIS
