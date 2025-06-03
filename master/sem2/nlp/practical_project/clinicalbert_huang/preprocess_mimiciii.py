import pandas as pd
import numpy as np
import re
import spacy
from datetime import timedelta # Not strictly needed with the fix, but good to have if manipulating deltas
import os
from tqdm import tqdm

# --- Configuration ---
MIMIC_DIR = './physionet.org/files/mimiciii/1.4/' # TODO: Update this path
OUTPUT_DIR = './'
NOTE_CATEGORY = 'Discharge summary'
EARLY_NOTES_HOURS_MAX = None
MIN_STAY_HOURS_FOR_EARLY_NOTES = 24

os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading SpaCy en_core_web_sm model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\[\*\*.*?\*\*\]', '', text)
    text = re.sub(r'\r\n|\r|\n', ' ', text)
    text = re.sub(r'==+', '', text)
    text = re.sub(r'--+', '', text)
    text = re.sub(r'm\.d\.', 'md', text)
    text = re.sub(r'dr\.', 'dr', text)
    text = re.sub(r'\b\d+\.\s', '', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text

print("Loading MIMIC-III CSVs...")
admissions_df = pd.read_csv(os.path.join(MIMIC_DIR, 'ADMISSIONS.csv'))
patients_df = pd.read_csv(os.path.join(MIMIC_DIR, 'PATIENTS.csv'))
# You can add dtype={'CHARTDATE': str, 'CHARTTIME': str} or low_memory=False to handle DtypeWarning robustly
# For now, we let it warn, as errors='coerce' will handle parsing issues.
notes_df = pd.read_csv(os.path.join(MIMIC_DIR, 'NOTEEVENTS.csv'))

print("Preprocessing admissions data...")

# Convert date columns to datetime objects, coercing errors to NaT
admissions_df['ADMITTIME'] = pd.to_datetime(admissions_df['ADMITTIME'], errors='coerce')
admissions_df['DISCHTIME'] = pd.to_datetime(admissions_df['DISCHTIME'], errors='coerce')
admissions_df['DEATHTIME'] = pd.to_datetime(admissions_df['DEATHTIME'], errors='coerce')
patients_df['DOB'] = pd.to_datetime(patients_df['DOB'], errors='coerce')
patients_df['DOD'] = pd.to_datetime(patients_df['DOD'], errors='coerce') # Though not directly used for age

# Merge admissions with patient data to get DOB
admissions_df = admissions_df.merge(patients_df[['SUBJECT_ID', 'DOB']], on='SUBJECT_ID', how='left') # Reduced columns from patients_df

# Initial cleaning of date inconsistencies
admissions_df.dropna(subset=['ADMITTIME', 'DOB'], inplace=True) # Remove rows where ADMITTIME or DOB is NaT
admissions_df = admissions_df[admissions_df['DOB'] <= admissions_df['ADMITTIME']] # Ensure DOB is not after ADMITTIME

# Robust ADMIT_AGE calculation using underlying int64 nanosecond values
# Get nanoseconds since epoch for ADMITTIME and DOB
# .values accesses the numpy array, .astype(np.int64) converts datetime64[ns] to int64
nanoseconds_admit = admissions_df['ADMITTIME'].values.astype(np.int64)
nanoseconds_dob = admissions_df['DOB'].values.astype(np.int64)

# Calculate difference in nanoseconds
delta_nanoseconds = nanoseconds_admit - nanoseconds_dob

# Define nanoseconds per day as an int64 to prevent overflow in intermediate products if it were float
NANOSECONDS_IN_A_DAY = np.int64(24 * 60 * 60 * 1_000_000_000)

# Calculate age in days (float division)
delta_days = delta_nanoseconds / NANOSECONDS_IN_A_DAY

admissions_df['ADMIT_AGE'] = delta_days / 365.25

# Filter out newborn admissions (age < 1 year)
admissions_df = admissions_df[admissions_df['ADMIT_AGE'] >= 1]
print(f"Admissions after filtering newborns: {len(admissions_df)}")

# Filter out admissions with in-hospital death
admissions_df = admissions_df[admissions_df['HOSPITAL_EXPIRE_FLAG'] == 0]
print(f"Admissions after filtering in-hospital deaths: {len(admissions_df)}")

# Prepare notes_df date columns
notes_df['CHARTTIME'] = pd.to_datetime(notes_df['CHARTTIME'], errors='coerce')
notes_df['CHARTDATE'] = pd.to_datetime(notes_df['CHARTDATE'], errors='coerce')

# ... (rest of your script: Calculate 30-day readmission labels..., etc.) ...
print("Calculating 30-day readmission labels...")
admissions_df = admissions_df.sort_values(['SUBJECT_ID', 'ADMITTIME'])
admissions_df['NEXT_ADMITTIME'] = admissions_df.groupby('SUBJECT_ID')['ADMITTIME'].shift(-1)
admissions_df['DAYS_TO_NEXT_ADMIT'] = (admissions_df['NEXT_ADMITTIME'] - admissions_df['DISCHTIME']).dt.total_seconds() / (24 * 60 * 60)
admissions_df['READMISSION_30D'] = (admissions_df['DAYS_TO_NEXT_ADMIT'] <= 30).astype(int)

print(f"Filtering notes...")
if NOTE_CATEGORY:
    notes_df_filtered = notes_df[notes_df['CATEGORY'] == NOTE_CATEGORY].copy() # Use .copy() to avoid SettingWithCopyWarning
    print(f"Notes after filtering for category '{NOTE_CATEGORY}': {len(notes_df_filtered)}")
elif EARLY_NOTES_HOURS_MAX is not None:
    notes_df_merged = notes_df.merge(admissions_df[['HADM_ID', 'ADMITTIME', 'DISCHTIME']], on='HADM_ID', how='left')
    notes_df_merged.dropna(subset=['ADMITTIME', 'CHARTTIME'], inplace=True)
    
    notes_df_merged['HOURS_FROM_ADMISSION'] = (notes_df_merged['CHARTTIME'] - notes_df_merged['ADMITTIME']).dt.total_seconds() / 3600
    
    notes_df_filtered = notes_df_merged[
        (notes_df_merged['HOURS_FROM_ADMISSION'] >= 0) & 
        (notes_df_merged['HOURS_FROM_ADMISSION'] <= EARLY_NOTES_HOURS_MAX)
    ].copy()
    print(f"Notes after filtering for first {EARLY_NOTES_HOURS_MAX} hours: {len(notes_df_filtered)}")

    if MIN_STAY_HOURS_FOR_EARLY_NOTES:
        admissions_df['STAY_DURATION_HOURS'] = (admissions_df['DISCHTIME'] - admissions_df['ADMITTIME']).dt.total_seconds() / 3600
        valid_hadm_ids_early_notes = admissions_df[admissions_df['STAY_DURATION_HOURS'] > MIN_STAY_HOURS_FOR_EARLY_NOTES]['HADM_ID']
        admissions_df = admissions_df[admissions_df['HADM_ID'].isin(valid_hadm_ids_early_notes)]
        # Filter notes_df_filtered again to only include these valid admissions
        notes_df_filtered = notes_df_filtered[notes_df_filtered['HADM_ID'].isin(valid_hadm_ids_early_notes)]
        print(f"Admissions after filtering out short stays (<{MIN_STAY_HOURS_FOR_EARLY_NOTES}h) for early notes task: {len(admissions_df)}")
        print(f"Notes after filtering for valid HADM_IDs in early notes task: {len(notes_df_filtered)}")
else:
    print("WARNING: No specific note category or early notes time window specified. Using all notes.")
    notes_df_filtered = notes_df.copy()


notes_df_to_agg = notes_df_filtered[['HADM_ID', 'TEXT']] # Ensure using the filtered df
print("Aggregating notes per admission...")
# Check if notes_df_to_agg is empty
if notes_df_to_agg.empty:
    print("Warning: No notes found after filtering. Final dataframe will be empty.")
    final_df = pd.DataFrame(columns=['HADM_ID', 'SUBJECT_ID', 'TEXT', 'READMISSION_30D']) # Create empty df with expected columns
else:
    notes_aggregated_df = notes_df_to_agg.groupby('HADM_ID')['TEXT'].apply(lambda x: ' '.join(x)).reset_index()
    final_df = admissions_df.merge(notes_aggregated_df, on='HADM_ID', how='inner')

print(f"Total admissions with notes for the task: {len(final_df)}")
if len(final_df) == 0 and not notes_df_to_agg.empty : # Added check to avoid error if notes_df_to_agg was empty
    # This condition might be hit if admissions_df became empty or no common HADM_ID
    print("Warning: No admissions remaining after merging with aggregated notes. Check filter criteria.")
    # Create an empty DataFrame with expected columns to prevent error in subsequent steps
    final_df_to_save = pd.DataFrame(columns=['HADM_ID', 'SUBJECT_ID', 'text', 'label'])
elif final_df.empty: # Handles case where notes_df_to_agg was empty from start
    final_df_to_save = pd.DataFrame(columns=['HADM_ID', 'SUBJECT_ID', 'text', 'label'])
else:
    print("Applying text cleaning and segmentation...")
    tqdm.pandas(desc="Cleaning Text")
    final_df['CLEANED_TEXT'] = final_df['TEXT'].progress_apply(clean_text)
    final_df_to_save = final_df[['HADM_ID', 'SUBJECT_ID', 'CLEANED_TEXT', 'READMISSION_30D']].copy()
    final_df_to_save.rename(columns={'CLEANED_TEXT': 'text', 'READMISSION_30D': 'label'}, inplace=True)

output_path = os.path.join(OUTPUT_DIR, 'processed_readmission_data.parquet')
final_df_to_save.to_parquet(output_path, index=False)
print(f"Processed data saved to {output_path}")

if not final_df_to_save.empty:
    print(f"Number of positive readmission labels: {final_df_to_save['label'].sum()}")
    print(f"Number of negative readmission labels: {len(final_df_to_save) - final_df_to_save['label'].sum()}")
else:
    print("Resulting DataFrame is empty. No labels to count.")

print("Preprocessing complete.")
