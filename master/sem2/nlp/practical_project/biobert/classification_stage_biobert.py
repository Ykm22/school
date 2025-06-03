import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import os
import logging
from datetime import timedelta

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score

# --- Configuration ---
MIMIC_III_DIR = '../physionet.org/files/mimiciii/1.4' # IMPORTANT: Update this path
ADMISSIONS_FILE = os.path.join(MIMIC_III_DIR, 'ADMISSIONS.csv')
NOTEEVENTS_FILE = os.path.join(MIMIC_III_DIR, 'NOTEEVENTS.csv')

OUTPUT_DIR = './classification_output'
MODEL_CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, 'checkpoints')
LOG_FILE = os.path.join(OUTPUT_DIR, 'classification_log.txt')
RESULTS_FILE = os.path.join(OUTPUT_DIR, 'results.txt')
LOSS_PROGRESSION_FILE = os.path.join(OUTPUT_DIR, 'loss_progression.csv')

BIOBERT_MODEL_NAME = 'dmis-lab/biobert-base-cased-v1.1' # or 'dmis-lab/biobert-v1.1'

# For sampling data to test the script quickly
# Set SAMPLE_PATIENTS_N to a small number (e.g., 1000) for quick testing.
# Set to None to use all patients.
SAMPLE_PATIENTS_N = None # Process notes from N patients
MAX_SEQ_LENGTH = 512  # Max sequence length for BioBERT
BATCH_SIZE = 8      # Adjust based on GPU memory (e.g., 4, 8, 16)
ACCUMULATION_STEPS = 8
EFFECTIVE_BATCH_SIZE = BATCH_SIZE * ACCUMULATION_STEPS
EPOCHS = 3           # As per paper (Table 1)
LEARNING_RATE = 2e-5 # As per paper (Table 1 for BioBERT)
RANDOM_SEED = 42

# --- Setup Logging & Directories ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_CHECKPOINT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# --- Download NLTK stopwords if not present ---
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# --- Text Preprocessing Function (as per paper's Section 4.2) ---
def preprocess_text_classification(text):
    if not isinstance(text, str):
        return ""
    # Text cleaning: remove non-essential info (e.g., de-id tags)
    text = re.sub(r'\[\*\*.*?\*\*\]', '', text) # Remove MIMIC de-identification placeholders
    # Standardized by converting to lowercase
    text = text.lower()
    # Extraneous elements like punctuation, special characters are removed
    # This is a bit aggressive; clinical text might have important punctuation.
    # The paper says "punctuation, special characters". BERT tokenizers handle much of this.
    # For this implementation, we'll be less aggressive than the NER script's preprocessing
    # and let the BioBERT tokenizer handle more.
    # text = re.sub(r'[^a-z0-9\s]', '', text) # Paper's description
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace

    # Stop words removal (Paper mentions it. Often not strictly needed for transformers but following paper)
    # words = text.split()
    # words = [word for word in words if word not in stop_words]
    # text = " ".join(words) # Disabling this for classification as BioBERT tokenizer is robust
    return text


# --- PyTorch Dataset Class ---
class ReadmissionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# --- Helper Functions ---
def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def compute_metrics(preds, labels):
    preds_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    precision, recall, f1, _ = precision_recall_fscore_support(labels_flat, preds_flat, average='binary', zero_division=0)
    acc = accuracy_score(labels_flat, preds_flat)
    try:
        auc = roc_auc_score(labels_flat, preds[:, 1]) # Probability of positive class
    except ValueError: # Happens if only one class present in a batch/fold
        auc = 0.0
        logging.warning("AUC calculation failed due to only one class present in labels.")

    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall,
        'auc': auc
    }

# --- Training Function ---
def train_epoch(model, data_loader, optimizer, device, scheduler, accumulation_steps=1): # Added accumulation_steps
    model.train()
    total_original_loss = 0.0  # To sum original scale losses for reporting average epoch loss
    
    # For metrics calculation
    all_preds_list = [] 
    all_labels_list = []

    optimizer.zero_grad() # Zero gradients at the beginning of the epoch / first accumulation cycle

    for batch_idx, batch in enumerate(data_loader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        # Forward pass
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        loss = outputs.loss # This is the loss for the current micro-batch
        logits = outputs.logits

        # Store original loss for epoch-level reporting
        total_original_loss += loss.item()

        # Scale loss for gradient accumulation
        # If accumulation_steps is 1, this doesn't change the loss.
        scaled_loss = loss / accumulation_steps 
        
        # Backward pass to accumulate gradients
        scaled_loss.backward() 

        # Store predictions and labels from this micro-batch for metric calculation later
        all_preds_list.append(logits.detach().cpu().numpy())
        all_labels_list.append(labels.detach().cpu().numpy())

        # Perform optimizer step only after accumulating gradients for 'accumulation_steps' micro-batches
        # Also step if it's the last batch of the epoch
        if (batch_idx + 1) % accumulation_steps == 0 or (batch_idx + 1) == len(data_loader):
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0) # Clip gradients just before optimizer step
            optimizer.step()    # Update weights
            scheduler.step()    # Update learning rate (if it's a step-wise scheduler)
            optimizer.zero_grad() # Reset gradients for the next accumulation cycle

        # Logging (optional, can be less frequent or adjusted)
        # Log the original loss of the current micro-batch
        if batch_idx > 0 and batch_idx % (max(1, len(data_loader) // 10)) == 0: # Log roughly 10 times per epoch
            logging.info(f"  Micro-batch {batch_idx+1}/{len(data_loader)}, Current Micro-batch Loss: {loss.item():.4f}")

    # Concatenate all predictions and labels from the epoch
    if not all_preds_list: # Handle cases where data_loader might be empty
        logging.warning("No predictions made in train_epoch, possibly empty data_loader.")
        # Return default or error values
        return 0.0, {'accuracy': 0, 'f1': 0, 'precision': 0, 'recall': 0, 'auc': 0}
        
    final_preds = np.concatenate(all_preds_list, axis=0)
    final_labels = np.concatenate(all_labels_list, axis=0)
    
    avg_epoch_loss = total_original_loss / len(data_loader) # Average loss per micro-batch processed
    metrics = compute_metrics(final_preds, final_labels)
    
    return avg_epoch_loss, metrics

# --- Evaluation Function ---
def eval_model(model, data_loader, device, loss_fn):
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
            logits = outputs.logits

            total_loss += loss.item()
            all_preds.extend(logits.detach().cpu().numpy())
            all_labels.extend(labels.detach().cpu().numpy())

    avg_loss = total_loss / len(data_loader)
    metrics = compute_metrics(np.array(all_preds), np.array(all_labels))
    return avg_loss, metrics


# --- Main Classification Workflow ---
def main_classification():
    logging.info("Starting Classification Stage...")
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(RANDOM_SEED)

    device = get_device()
    logging.info(f"Using device: {device}")

    # Load Tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL_NAME)
        logging.info(f"Tokenizer {BIOBERT_MODEL_NAME} loaded.")
    except Exception as e:
        logging.error(f"Error loading tokenizer: {e}")
        return

    # 1. Load Data
    logging.info("Loading ADMISSIONS and NOTEEVENTS data...")
    try:
        admissions_df = pd.read_csv(ADMISSIONS_FILE, parse_dates=['ADMITTIME', 'DISCHTIME'])
        # Using iterator and chunksize for NOTEEVENTS
        chunk_iter_notes = pd.read_csv(NOTEEVENTS_FILE, usecols=['SUBJECT_ID', 'HADM_ID', 'CATEGORY', 'TEXT'], chunksize=50000)
        notes_df_list = []
        for chunk in chunk_iter_notes:
            # Focusing on Discharge Summaries as they are most comprehensive for readmission
            # The paper is vague, "unstructured clinical notes". Discharge summaries are a common choice.
            notes_df_list.append(chunk[chunk['CATEGORY'] == 'Discharge summary'].copy())
        notes_df = pd.concat(notes_df_list, ignore_index=True)
        logging.info(f"Loaded {len(admissions_df)} admissions and {len(notes_df)} discharge summaries.")
    except FileNotFoundError:
        logging.error(f"MIMIC-III CSV files not found in {MIMIC_III_DIR}. Please check paths.")
        return
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    # --- Data Sampling (Optional) ---
    if SAMPLE_PATIENTS_N is not None:
        logging.info(f"Sampling data for {SAMPLE_PATIENTS_N} patients for quick testing.")
        unique_patients = admissions_df['SUBJECT_ID'].unique()
        if SAMPLE_PATIENTS_N < len(unique_patients):
            sampled_patient_ids = np.random.choice(unique_patients, SAMPLE_PATIENTS_N, replace=False)
            admissions_df = admissions_df[admissions_df['SUBJECT_ID'].isin(sampled_patient_ids)]
            notes_df = notes_df[notes_df['SUBJECT_ID'].isin(sampled_patient_ids)]
            logging.info(f"Sampled to {len(admissions_df)} admissions and {len(notes_df)} notes for these patients.")


    # 2. Define Readmission Labels
    logging.info("Defining 30-day readmission labels...")
    admissions_df = admissions_df.sort_values(['SUBJECT_ID', 'ADMITTIME'])
    admissions_df['NEXT_ADMITTIME'] = admissions_df.groupby('SUBJECT_ID')['ADMITTIME'].shift(-1)
    admissions_df['DAYS_TO_NEXT_ADMIT'] = (admissions_df['NEXT_ADMITTIME'] - admissions_df['DISCHTIME']).dt.total_seconds() / (24 * 60 * 60)
    admissions_df['READMISSION_30D'] = ((admissions_df['DAYS_TO_NEXT_ADMIT'] > 0) & (admissions_df['DAYS_TO_NEXT_ADMIT'] <= 30)).astype(int)
    
    # Filter out elective admissions for readmission definition, as per common practice
    # The paper doesn't specify, but unplanned readmissions are usually the target.
    # Let's assume any readmission within 30 days is the target as per paper simplicity.

    # 3. Merge notes with admission data
    # Aggregate notes per admission if multiple discharge summaries exist (unlikely but possible)
    notes_df_agg = notes_df.groupby('HADM_ID')['TEXT'].apply(lambda x: ' '.join(x)).reset_index()
    
    df = pd.merge(admissions_df, notes_df_agg, on='HADM_ID', how='inner') # Inner join to keep only admissions with notes
    df = df.dropna(subset=['TEXT', 'READMISSION_30D']) # Ensure text and label are present
    df = df[['HADM_ID', 'SUBJECT_ID', 'TEXT', 'READMISSION_30D']].copy()

    if df.empty:
        logging.error("No data remaining after merging admissions and notes, or after filtering. Check data processing steps.")
        return
    logging.info(f"Data prepared: {len(df)} records with text and readmission labels.")
    logging.info(f"Readmission distribution: \n{df['READMISSION_30D'].value_counts(normalize=True)}")


    # 4. Preprocess Text
    logging.info("Preprocessing text data...")
    df['processed_text'] = df['TEXT'].apply(preprocess_text_classification)
    
    # Keep only necessary columns
    df_final = df[['processed_text', 'READMISSION_30D']].rename(columns={'processed_text': 'text', 'READMISSION_30D': 'label'})


    # 5. Train/Validation/Test Split
    # First, split into train+val and test
    train_val_df, test_df = train_test_split(df_final, test_size=0.2, random_state=RANDOM_SEED, stratify=df_final['label'])
    # Then, split train+val into train and val
    train_df, val_df = train_test_split(train_val_df, test_size=0.125, random_state=RANDOM_SEED, stratify=train_val_df['label']) # 0.125 * 0.8 = 0.1 (10% of total for val)

    logging.info(f"Train size: {len(train_df)}, Validation size: {len(val_df)}, Test size: {len(test_df)}")
    logging.info(f"Train distribution:\n{train_df['label'].value_counts(normalize=True)}")
    logging.info(f"Validation distribution:\n{val_df['label'].value_counts(normalize=True)}")
    logging.info(f"Test distribution:\n{test_df['label'].value_counts(normalize=True)}")

    # Create Datasets and DataLoaders
    train_dataset = ReadmissionDataset(
        texts=train_df['text'].to_numpy(),
        labels=train_df['label'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_SEQ_LENGTH
    )
    val_dataset = ReadmissionDataset(
        texts=val_df['text'].to_numpy(),
        labels=val_df['label'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_SEQ_LENGTH
    )
    test_dataset = ReadmissionDataset(
        texts=test_df['text'].to_numpy(),
        labels=test_df['label'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_SEQ_LENGTH
    )

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, num_workers=2)


    # 6. Model Initialization
    try:
        model = AutoModelForSequenceClassification.from_pretrained(
            BIOBERT_MODEL_NAME,
            num_labels=2 # Binary classification: Readmitted / Not Readmitted
        )
        model.to(device)
        logging.info(f"Model {BIOBERT_MODEL_NAME} loaded for sequence classification.")
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return

    # 7. Optimizer and Scheduler
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, eps=1e-8) # eps from BERT paper
    total_steps = len(train_loader) * EPOCHS

    num_micro_batches_per_epoch = len(train_loader)
    num_optimizer_steps_per_epoch = num_micro_batches_per_epoch // ACCUMULATION_STEPS
    if num_micro_batches_per_epoch % ACCUMULATION_STEPS != 0:
        num_optimizer_steps_per_epoch += 1 # for the last partial accumulation set

    total_optimizer_steps = num_optimizer_steps_per_epoch * EPOCHS

    logging.info(f"Number of micro-batches per epoch: {num_micro_batches_per_epoch}")
    logging.info(f"Number of optimizer steps per epoch: {num_optimizer_steps_per_epoch}")
    logging.info(f"Total optimizer steps for scheduler: {total_optimizer_steps}")

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0, # Or set to e.g. 0.1 * total_steps
        num_training_steps=total_optimizer_steps
    )
    loss_fn = torch.nn.CrossEntropyLoss().to(device) # Already handled by HuggingFace model if labels are passed

    # 8. Training Loop
    logging.info("Starting training...")
    best_val_auc = 0.0 # Or use F1, or val_loss
    loss_progression_data = []

    for epoch in range(EPOCHS):
        logging.info(f"--- Epoch {epoch + 1}/{EPOCHS} ---")
        train_loss, train_metrics = train_epoch(model, train_loader, optimizer, device, scheduler, accumulation_steps=ACCUMULATION_STEPS)
        logging.info(f"Epoch {epoch + 1} Train Loss: {train_loss:.4f}, Train Metrics: {train_metrics}")

        val_loss, val_metrics = eval_model(model, val_loader, device, loss_fn)
        logging.info(f"Epoch {epoch + 1} Val Loss: {val_loss:.4f}, Val Metrics: {val_metrics}")

        loss_progression_data.append({
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'val_loss': val_loss,
            'train_accuracy': train_metrics['accuracy'],
            'val_accuracy': val_metrics['accuracy'],
            'train_f1': train_metrics['f1'],
            'val_f1': val_metrics['f1'],
            'train_auc': train_metrics['auc'],
            'val_auc': val_metrics['auc'],
        })

        if val_metrics['auc'] > best_val_auc: # Using AUC for best model, as in paper
            best_val_auc = val_metrics['auc']
            model_save_path = os.path.join(MODEL_CHECKPOINT_DIR, f"best_model_epoch_{epoch+1}.pt")
            torch.save(model.state_dict(), model_save_path)
            logging.info(f"New best model saved to {model_save_path} with Val AUC: {best_val_auc:.4f}")

    # Save loss progression
    loss_df = pd.DataFrame(loss_progression_data)
    loss_df.to_csv(LOSS_PROGRESSION_FILE, index=False)
    logging.info(f"Loss progression saved to {LOSS_PROGRESSION_FILE}")

    # 9. Evaluation on Test Set (using the last model or best saved model)
    # For simplicity, using the model from the last epoch.
    # To load best model: model.load_state_dict(torch.load(PATH_TO_BEST_MODEL_PT))
    logging.info("Evaluating on Test Set...")
    test_loss, test_metrics = eval_model(model, test_loader, device, loss_fn)
    logging.info(f"Test Loss: {test_loss:.4f}")
    logging.info(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    logging.info(f"Test Precision: {test_metrics['precision']:.4f}")
    logging.info(f"Test Recall: {test_metrics['recall']:.4f}")
    logging.info(f"Test F1-score: {test_metrics['f1']:.4f}")
    logging.info(f"Test AUC-ROC: {test_metrics['auc']:.4f}") # This is the key metric from paper

    # 10. Save Results
    with open(RESULTS_FILE, 'w') as f:
        f.write("--- Model Configuration ---\n")
        f.write(f"Model Name: {BIOBERT_MODEL_NAME}\n")
        f.write(f"Max Sequence Length: {MAX_SEQ_LENGTH}\n")
        f.write(f"Batch Size: {BATCH_SIZE}\n")
        f.write(f"Epochs: {EPOCHS}\n")
        f.write(f"Learning Rate: {LEARNING_RATE}\n")
        f.write("\n--- Test Set Performance ---\n")
        f.write(f"Test Loss: {test_loss:.4f}\n")
        for key, value in test_metrics.items():
            f.write(f"Test {key.capitalize()}: {value:.4f}\n")

    logging.info(f"Results saved to {RESULTS_FILE}")
    logging.info("Classification Stage finished.")

if __name__ == '__main__':
    main_classification()
