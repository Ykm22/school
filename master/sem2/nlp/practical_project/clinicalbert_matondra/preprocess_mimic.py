import pandas as pd
import numpy as np
from datetime import timedelta
import re
import spacy
import logging
from tqdm import tqdm

# --- Configuration ---
MIMIC_DIR = '../physionet.org/files/mimiciii/1.4/' # ADJUST THIS PATH
ADMISSIONS_FILE = MIMIC_DIR + 'ADMISSIONS.csv'
NOTEEVENTS_FILE = MIMIC_DIR + 'NOTEEVENTS.csv'
OUTPUT_PROCESSED_FILE = './processed_mimic_data_for_readmission.parquet' # Using parquet for efficiency

DAYS_FOR_READMISSION_WINDOW = 30 # Check for readmission within 30 days
DAYS_OF_NOTES_TO_CONSIDER = 5   # Use notes from the first 5 days of admission
MIN_NOTES_LENGTH = 20 # Minimum number of words for a note segment after cleaning

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# --- Load SpaCy Model ---
# Run: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) # Faster for sentence segmentation
    nlp.add_pipe('sentencizer') # EXPLICITLY ADD SENTENCIZER
    nlp.max_length = 2000000 # Increase if you have very long concatenated notes
except OSError:
    logging.error("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    exit()

def clean_text(text):
    """
    Cleans clinical text based on paper's description.
    """
    if not isinstance(text, str):
        return ""

    # Convert to Lowercase
    text = text.lower()
    # Remove Line Breaks and Carriage Returns
    text = text.replace('\n', ' ').replace('\r', ' ')
    # De-identify PII inside brackets (e.g., [** ... **])
    text = re.sub(r'\[\*\*.*?\*\*\]', '[PHI]', text)
    # Remove special characters (keep alphanumeric, spaces, and essential punctuation like periods for sentence segmentation)
    text = re.sub(r'[^a-z0-9\s\.]', '', text) # Basic cleaning, might need refinement
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def segment_and_filter_sentences(doc_text):
    """
    Segments text into sentences using SpaCy and filters short sentences.
    The paper mentions: "segmentations that have less than 20 words are fused into
    the previous segmentation so that they are not singled out as different sentences."
    This implementation will filter out short sentences instead of fusing for simplicity.
    A more complex fusion logic could be added if needed.
    """
    doc = nlp(doc_text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip().split()) >= MIN_NOTES_LENGTH]
    return " ".join(sentences) # Join filtered sentences back

def main():
    logging.info("Starting MIMIC-III data preprocessing for readmission prediction.")

    # 1. Load ADMISSIONS table
    logging.info(f"Loading {ADMISSIONS_FILE}...")
    admissions = pd.read_csv(ADMISSIONS_FILE)
    logging.info(f"Loaded {len(admissions)} admission records.")

    # Convert date columns to datetime
    admissions['ADMITTIME'] = pd.to_datetime(admissions['ADMITTIME'], errors='coerce')
    admissions['DISCHTIME'] = pd.to_datetime(admissions['DISCHTIME'], errors='coerce')
    admissions['DEATHTIME'] = pd.to_datetime(admissions['DEATHTIME'], errors='coerce')

    # Filter: Remove 'NEWBORN' admissions
    admissions = admissions[admissions['ADMISSION_TYPE'] != 'NEWBORN']
    logging.info(f"Admissions after removing NEWBORN: {len(admissions)}")

    # Filter: Keep only 'EMERGENCY' and 'URGENT' admissions as per paper
    admissions = admissions[admissions['ADMISSION_TYPE'].isin(['EMERGENCY', 'URGENT'])]
    logging.info(f"Admissions after filtering for EMERGENCY/URGENT: {len(admissions)}")
    
    # Filter: Remove admissions where DEATHTIME is not null (focus is on readmission, not mortality during this admission)
    admissions = admissions[admissions['DEATHTIME'].isnull()]
    logging.info(f"Admissions after removing those with DEATHTIME: {len(admissions)}")

    # Drop rows with missing critical time data after initial filtering
    admissions.dropna(subset=['SUBJECT_ID', 'HADM_ID', 'ADMITTIME', 'DISCHTIME'], inplace=True)
    logging.info(f"Admissions after dropping NaNs in key time columns: {len(admissions)}")

    # Sort by subject_id and admittime to identify readmissions
    admissions = admissions.sort_values(['SUBJECT_ID', 'ADMITTIME'])

    # 2. Create Readmission Label
    logging.info(f"Calculating readmission label (within {DAYS_FOR_READMISSION_WINDOW} days)...")
    admissions['NEXT_ADMITTIME'] = admissions.groupby('SUBJECT_ID')['ADMITTIME'].shift(-1)
    admissions['NEXT_ADMISSION_TYPE'] = admissions.groupby('SUBJECT_ID')['ADMISSION_TYPE'].shift(-1) # Optional: if readmission needs to be of specific type

    # Calculate days to next admission
    admissions['DAYS_TO_NEXT_ADMISSION'] = (admissions['NEXT_ADMITTIME'] - admissions['DISCHTIME']).dt.total_seconds() / (24 * 60 * 60)

    # Define readmission: next admission within X days (and ensure it's not the same day if data is noisy)
    admissions['READMITTED_30D'] = (
        (admissions['DAYS_TO_NEXT_ADMISSION'] >= 0) & \
        (admissions['DAYS_TO_NEXT_ADMISSION'] < DAYS_FOR_READMISSION_WINDOW)
    ).astype(int)
    
    logging.info(f"Number of readmissions within {DAYS_FOR_READMISSION_WINDOW} days: {admissions['READMITTED_30D'].sum()}")
    logging.info(f"Readmission rate: {admissions['READMITTED_30D'].mean():.4f}")

    # Select relevant columns from admissions
    admissions_processed = admissions[['SUBJECT_ID', 'HADM_ID', 'ADMITTIME', 'DISCHTIME', 'ADMISSION_TYPE', 'READMITTED_30D']].copy()

    # 3. Load NOTEEVENTS table
    logging.info(f"Loading {NOTEEVENTS_FILE}...")
    # For memory efficiency, load only necessary columns and filter progressively
    # If NOTEEVENTS is too large, consider chunking or Dask
    notes_cols = ['SUBJECT_ID', 'HADM_ID', 'CHARTDATE', 'CHARTTIME', 'CATEGORY', 'TEXT']
    notes = pd.read_csv(NOTEEVENTS_FILE, usecols=notes_cols)
    logging.info(f"Loaded {len(notes)} note events.")

    # Filter notes for HADM_IDs present in our processed admissions
    notes = notes[notes['HADM_ID'].isin(admissions_processed['HADM_ID'])]
    logging.info(f"Notes after filtering for relevant HADM_IDs: {len(notes)}")
    
    # Exclude discharge summaries as per paper ("excluding discharge notes")
    notes = notes[notes['CATEGORY'].str.upper() != 'DISCHARGE SUMMARY']
    logging.info(f"Notes after excluding 'Discharge Summary' category: {len(notes)}")

    # Convert note chart times
    # CHARTTIME can be NaN, CHARTDATE should always be present for notes.
    notes['CHARTTIME'] = pd.to_datetime(notes['CHARTTIME'], errors='coerce')
    notes['CHARTDATE'] = pd.to_datetime(notes['CHARTDATE'], errors='coerce')
    
    # Use CHARTTIME if available, otherwise CHARTDATE (setting time to midnight for CHARTDATE-only cases)
    notes['NOTE_DATETIME'] = notes['CHARTTIME']
    # For rows where CHARTTIME is NaT, use CHARTDATE.
    # Ensure CHARTDATE is not NaT before using it.
    notes.loc[notes['NOTE_DATETIME'].isnull() & notes['CHARTDATE'].notnull(), 'NOTE_DATETIME'] = notes.loc[notes['NOTE_DATETIME'].isnull() & notes['CHARTDATE'].notnull(), 'CHARTDATE']

    notes.dropna(subset=['NOTE_DATETIME', 'HADM_ID', 'TEXT'], inplace=True) # Ensure critical fields are not null
    logging.info(f"Notes after handling and dropping NaNs in NOTE_DATETIME: {len(notes)}")


    # 4. Merge notes with admissions to get ADMITTIME for filtering
    notes_merged = pd.merge(notes[['HADM_ID', 'TEXT', 'NOTE_DATETIME']],
                            admissions_processed[['HADM_ID', 'ADMITTIME']],
                            on='HADM_ID', how='left')

    # Filter notes to be within the first N days of admission
    # ADMITTIME + timedelta(days=DAYS_OF_NOTES_TO_CONSIDER) is the cutoff
    time_cutoff = notes_merged['ADMITTIME'] + timedelta(days=DAYS_OF_NOTES_TO_CONSIDER)
    notes_filtered = notes_merged[notes_merged['NOTE_DATETIME'] < time_cutoff]
    logging.info(f"Notes after filtering for first {DAYS_OF_NOTES_TO_CONSIDER} days of admission: {len(notes_filtered)}")

    # 5. Process and aggregate notes
    # Group by HADM_ID and concatenate notes, then clean and segment
    logging.info("Aggregating, cleaning, and segmenting notes for each admission...")
    
    aggregated_notes_text = []
    hadm_ids_for_notes = []

    # Use tqdm for progress bar
    for hadm_id, group in tqdm(notes_filtered.groupby('HADM_ID'), desc="Processing Notes"):
        # Concatenate all notes for this admission, sorted by time (implicitly by order in df if sorted prior)
        full_note_text = " ".join(group['TEXT'].astype(str).tolist())
        cleaned_note = clean_text(full_note_text)
        
        # The paper applies segmentation to each note, then potentially fuses.
        # Here, we concatenate, then clean, then segment the whole block.
        # If individual note segmentation is desired before concatenation, logic would be different.
        # Based on "Segment Each Note", this might imply cleaning/segmenting before concat.
        # Let's try cleaning THEN segmenting the concatenated block for now.
        # For very long texts, SpaCy might struggle. Let's assume it handles for now.
        # If SpaCy struggles, process notes individually then concatenate processed sentences.
        
        # If we want to segment each note individually then combine:
        # processed_sentences = []
        # for single_note_text in group['TEXT'].astype(str).tolist():
        #     cleaned_single_note = clean_text(single_note_text)
        #     if cleaned_single_note:
        #          processed_sentences.append(segment_and_filter_sentences(cleaned_single_note))
        # final_text = " ".join(s for s in processed_sentences if s) # Ensure no empty strings

        # Current approach: Concat -> Clean -> Segment
        if cleaned_note:
            final_text = segment_and_filter_sentences(cleaned_note) # Using segmentation
        else:
            final_text = ""

        if final_text: # Only add if there's content after processing
            aggregated_notes_text.append(final_text)
            hadm_ids_for_notes.append(hadm_id)

    notes_df_processed = pd.DataFrame({
        'HADM_ID': hadm_ids_for_notes,
        'processed_notes': aggregated_notes_text
    })
    logging.info(f"Processed notes for {len(notes_df_processed)} admissions.")

    # 6. Final Merge: admissions data with processed notes
    final_df = pd.merge(admissions_processed, notes_df_processed, on='HADM_ID', how='inner') # Inner join to keep only admissions with notes
    final_df.dropna(subset=['processed_notes'], inplace=True) # Remove rows where notes might be empty after all processing
    final_df = final_df[final_df['processed_notes'].str.strip() != '']

    logging.info(f"Final dataset size after merging with notes: {len(final_df)}")
    logging.info(f"Final readmission rate in dataset with notes: {final_df['READMITTED_30D'].mean():.4f}")

    if final_df.empty:
        logging.error("No data remaining after processing. Check filters and data paths.")
        return

    # 7. Save processed data
    logging.info(f"Saving processed data to {OUTPUT_PROCESSED_FILE}...")
    final_df.to_parquet(OUTPUT_PROCESSED_FILE, index=False)
    logging.info("Preprocessing complete.")

if __name__ == '__main__':
    main()
