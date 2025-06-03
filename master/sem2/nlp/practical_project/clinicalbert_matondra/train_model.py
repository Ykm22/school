import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
import logging
from tqdm import tqdm
import os

# --- Configuration ---
PROCESSED_DATA_FILE = './processed_mimic_data_for_readmission.parquet'
MODEL_NAME = 'emilyalsentzer/Bio_ClinicalBERT' # Or 'medicalai/ClinicalBERT' etc.
# MODEL_NAME = 'bert-base-uncased' # For faster testing if ClinicalBERT is too slow initially
MAX_LEN = 512  # Max sequence length for BERT
BATCH_SIZE = 8 # Adjust based on GPU memory (e.g., 4, 8, 16)
EPOCHS = 3     # Number of training epochs
LEARNING_RATE = 2e-5
RANDOM_SEED = 42
TRAIN_LOG_FILE = './training_log.txt'
MODEL_SAVE_PATH = './clinicalbert_readmission_model.bin'

# --- Logging Setup ---
# Remove basicConfig if it was set by preprocess, to avoid handler duplication if run in same session
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(TRAIN_LOG_FILE, mode='w'), # Log to file
                        logging.StreamHandler() # Log to console
                    ])

# --- Set Seed and Device ---
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.info(f"Using device: {device}")

# --- Custom Dataset ---
class AdmissionNotesDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = str(self.texts[item])
        label = self.labels[item]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False, # ClinicalBERT might not need them, check model specifics
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'text': text, # For inspection if needed
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# --- Model Training Function ---
def train_epoch(model, data_loader, loss_fn, optimizer, device, scheduler, n_examples):
    model = model.train()
    losses = []
    correct_predictions = 0
    
    # Use tqdm for progress bar
    pbar = tqdm(data_loader, desc=f"Training Epoch {epoch+1}/{EPOCHS}")
    for batch_idx, d in enumerate(pbar):
        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        labels = d["labels"].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels # Pass labels for built-in loss calculation
        )
        loss = outputs.loss
        logits = outputs.logits # Raw scores from the model

        _, preds = torch.max(logits, dim=1)
        correct_predictions += torch.sum(preds == labels)
        losses.append(loss.item())

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # Gradient clipping
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        
        # Update tqdm description with current loss
        if batch_idx % 10 == 0: # Log every 10 batches
            current_loss = np.mean(losses[-10:]) if len(losses) > 0 else loss.item()
            pbar.set_postfix({'loss': f'{current_loss:.4f}'})
            logging.info(f"Epoch {epoch+1}, Batch {batch_idx}/{len(data_loader)}, Batch Loss: {loss.item():.4f}, Avg Loss (last 10): {current_loss:.4f}")


    return correct_predictions.double() / n_examples, np.mean(losses)

# --- Model Evaluation Function ---
def eval_model(model, data_loader, loss_fn, device, n_examples):
    model = model.eval()
    losses = []
    correct_predictions = 0
    
    all_labels = []
    all_probs = [] # For AUC

    with torch.no_grad():
        pbar = tqdm(data_loader, desc="Evaluating")
        for d in pbar:
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            labels = d["labels"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
            logits = outputs.logits

            _, preds = torch.max(logits, dim=1)
            probs = torch.softmax(logits, dim=1)[:, 1] # Probability of positive class

            correct_predictions += torch.sum(preds == labels)
            losses.append(loss.item())
            
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    accuracy = correct_predictions.double() / n_examples
    avg_loss = np.mean(losses)
    
    # Calculate precision, recall, f1
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels, 
        np.array(all_probs) > 0.5, # Convert probs to binary predictions
        average='binary',
        zero_division=0
    )
    
    # Calculate AUC
    try:
        auc = roc_auc_score(all_labels, all_probs)
    except ValueError: # Happens if only one class is present in labels
        auc = 0.0 
        logging.warning("AUC calculation failed. Likely only one class in predictions or true labels during eval.")

    return accuracy, avg_loss, precision, recall, f1, auc


# --- Main Execution ---
if __name__ == '__main__':
    logging.info("Starting model training and evaluation process.")

    if not os.path.exists(PROCESSED_DATA_FILE):
        logging.error(f"Processed data file not found: {PROCESSED_DATA_FILE}. Run preprocess_mimic.py first.")
        exit()

    df = pd.read_parquet(PROCESSED_DATA_FILE)
    logging.info(f"Loaded processed data: {len(df)} records.")
    
    # Ensure there are enough samples for splitting
    if len(df) < 10: # Arbitrary small number
        logging.error(f"Not enough data to train ({len(df)} samples). Check preprocessing.")
        exit()
    
    # Ensure there's variability in the target variable if possible for stratified split
    if df['READMITTED_30D'].nunique() > 1:
        stratify_col = df['READMITTED_30D']
    else:
        stratify_col = None
        logging.warning("Target variable has only one unique value. Stratified split disabled.")

    # Split data: Train, Validation (Test set ideally separate, but for simplicity using val as test here)
    # The paper mentions "Split on patient admission level", which is what HADM_ID represents.
    # Using SUBJECT_ID for splitting would be a patient-level split across admissions.
    # Here, we split on the records (HADM_ID unique in final_df).
    df_train, df_val_test = train_test_split(
        df,
        test_size=0.3, # 70% train, 30% for val/test
        random_state=RANDOM_SEED,
        stratify=stratify_col
    )
    df_val, df_test = train_test_split(
        df_val_test,
        test_size=0.5, # Split the 30% into 15% val, 15% test
        random_state=RANDOM_SEED,
        stratify=df_val_test['READMITTED_30D'] if stratify_col is not None and df_val_test['READMITTED_30D'].nunique() > 1 else None
    )

    logging.info(f"Train size: {len(df_train)}, Validation size: {len(df_val)}, Test size: {len(df_test)}")
    logging.info(f"Train readmission rate: {df_train['READMITTED_30D'].mean():.4f}")
    logging.info(f"Validation readmission rate: {df_val['READMITTED_30D'].mean():.4f}")
    logging.info(f"Test readmission rate: {df_test['READMITTED_30D'].mean():.4f}")

    # Load tokenizer and model
    logging.info(f"Loading tokenizer and model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2) # 2 labels: not readmitted, readmitted
    model = model.to(device)

    # Create DataLoaders
    train_dataset = AdmissionNotesDataset(
        texts=df_train['processed_notes'].to_numpy(),
        labels=df_train['READMITTED_30D'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_LEN
    )
    train_data_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)

    val_dataset = AdmissionNotesDataset(
        texts=df_val['processed_notes'].to_numpy(),
        labels=df_val['READMITTED_30D'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_LEN
    )
    val_data_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, num_workers=2)
    
    test_dataset = AdmissionNotesDataset(
        texts=df_test['processed_notes'].to_numpy(),
        labels=df_test['READMITTED_30D'].to_numpy(),
        tokenizer=tokenizer,
        max_len=MAX_LEN
    )
    test_data_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, num_workers=2)

    # Optimizer and Scheduler
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    total_steps = len(train_data_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0, # Or a small fraction like 0.1 * total_steps
        num_training_steps=total_steps
    )

    # Loss function (CrossEntropyLoss is used by default when labels are passed to HuggingFace model)
    loss_fn = torch.nn.CrossEntropyLoss().to(device) # For manual calculation if needed, but usually not

    best_val_accuracy = 0
    history = {'train_acc': [], 'train_loss': [], 'val_acc': [], 'val_loss': [], 
               'val_precision': [], 'val_recall': [], 'val_f1': [], 'val_auc': []}

    logging.info("Starting training...")
    for epoch in range(EPOCHS):
        logging.info(f"--- Epoch {epoch + 1}/{EPOCHS} ---")
        train_acc, train_loss = train_epoch(
            model, train_data_loader, loss_fn, optimizer, device, scheduler, len(df_train)
        )
        logging.info(f"Train loss: {train_loss:.4f}, Train accuracy: {train_acc:.4f}")
        history['train_acc'].append(train_acc.item() if torch.is_tensor(train_acc) else train_acc)
        history['train_loss'].append(train_loss)

        val_acc, val_loss, val_prec, val_rec, val_f1, val_auc = eval_model(
            model, val_data_loader, loss_fn, device, len(df_val)
        )
        logging.info(f"Val loss: {val_loss:.4f}, Val accuracy: {val_acc:.4f}")
        logging.info(f"Val Precision: {val_prec:.4f}, Recall: {val_rec:.4f}, F1: {val_f1:.4f}, AUC: {val_auc:.4f}")
        
        history['val_acc'].append(val_acc.item() if torch.is_tensor(val_acc) else val_acc)
        history['val_loss'].append(val_loss)
        history['val_precision'].append(val_prec)
        history['val_recall'].append(val_rec)
        history['val_f1'].append(val_f1)
        history['val_auc'].append(val_auc)

        if val_acc > best_val_accuracy:
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            best_val_accuracy = val_acc
            logging.info(f"Best validation accuracy improved to {best_val_accuracy:.4f}. Model saved to {MODEL_SAVE_PATH}")

    logging.info("Training finished.")
    
    # --- Evaluate on Test Set with the best model ---
    logging.info("Loading best model for test set evaluation...")
    model.load_state_dict(torch.load(MODEL_SAVE_PATH)) # Load the best model
    model = model.to(device) # Ensure it's on the correct device

    logging.info("Evaluating on Test Set...")
    test_acc, test_loss, test_prec, test_rec, test_f1, test_auc = eval_model(
        model, test_data_loader, loss_fn, device, len(df_test)
    )
    logging.info(f"Test Loss: {test_loss:.4f}")
    logging.info(f"Test Accuracy: {test_acc:.4f}")
    logging.info(f"Test Precision: {test_prec:.4f}")
    logging.info(f"Test Recall: {test_rec:.4f}")
    logging.info(f"Test F1-Score: {test_f1:.4f}")
    logging.info(f"Test AUC: {test_auc:.4f}")

    # Log history for plotting
    logging.info(f"Training history: {history}")
    logging.info("Process complete. Training log saved to training_log.txt")
