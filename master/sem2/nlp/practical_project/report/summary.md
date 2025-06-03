# MIMIC-III Implementation Comparison

## Preprocessing Similarities
- **Data Sources**: All use MIMIC-III ADMISSIONS.csv and NOTEEVENTS.csv
- **Text Cleaning**: PII removal (bracket notation), lowercase conversion, whitespace normalization
- **Readmission Labels**: 30-day post-discharge window calculation
- **Output Format**: Parquet files for efficiency
- **Memory Management**: Progressive filtering and chunked data loading

## Preprocessing Differences

### Implementation 1 (ClinicalBERT Basic)
- **Note Selection**: Excludes discharge summaries, uses first 5 days only
- **Admission Filter**: EMERGENCY/URGENT only, excludes DEATHTIME cases
- **Text Processing**: SpaCy sentence segmentation, 20-word minimum segments
- **Age Handling**: Not explicitly processed

### Implementation 2 (Alternative)
- **Note Selection**: Configurable categories (default: discharge summaries)
- **Admission Filter**: Age ≥1 year, HOSPITAL_EXPIRE_FLAG==0
- **Text Processing**: Header standardization (M.D./Dr.), numbered list removal
- **Age Handling**: Nanosecond-precision datetime arithmetic

### Implementation 3 (NER Pipeline)
- **Note Selection**: Discharge summary/Physician/Nursing categories
- **Admission Filter**: Patient sampling for testing workflows
- **Text Processing**: NLTK stop word removal, aggressive special character filtering
- **Entity Focus**: Keyword-based medical entity extraction

### Implementation 4 (BioBERT Classification)
- **Note Selection**: Discharge summaries only, aggregated per admission
- **Admission Filter**: Optional patient sampling, no mortality exclusions
- **Text Processing**: Less aggressive cleaning, BioBERT tokenizer reliance
- **Data Strategy**: Chunked loading (50K rows), multiple summaries joined

## Training Similarities
- **Base Models**: Bio_ClinicalBERT or BioBERT variants
- **Task**: Binary classification for readmission prediction
- **Optimizer**: AdamW with 2e-5 learning rate
- **Epochs**: 3 training epochs
- **Sequence Length**: 512 tokens maximum
- **Gradient Clipping**: Max norm 1.0

## Training Differences

### Implementation 1 (Basic)
- **Architecture**: Standard HuggingFace classification head
- **Batch Size**: 8, no accumulation
- **Data Splits**: 70/15/15 train/val/test
- **Validation**: Best accuracy checkpoint
- **Metrics**: Accuracy, Precision, Recall, F1, AUC

### Implementation 2 (Cross-Validation)
- **Architecture**: Custom 768→2048→768→1 classifier head
- **Batch Size**: 8 with 7-step gradient accumulation
- **Data Splits**: 5-fold stratified cross-validation
- **Validation**: Best loss checkpoint with early stopping
- **Metrics**: AUROC, AUPRC, RP80 with patient aggregation (Equation 4)

### Implementation 3 (NER Focus)
- **Architecture**: Conceptual entity extraction (keyword-based placeholder)
- **Processing**: Entity categorization (symptoms, diagnoses, treatments, medications)
- **Output**: Entity dictionaries per note
- **Purpose**: Preprocessing stage for downstream classification

### Implementation 4 (Production-Ready)
- **Architecture**: Standard HuggingFace classification
- **Batch Size**: 8 with 8-step gradient accumulation (effective 64)
- **Data Splits**: 70/10/20 train/val/test
- **Validation**: Best AUC checkpoint
- **Metrics**: AUC-ROC primary, comprehensive classification metrics
- **Features**: Loss progression tracking, robust error handling
