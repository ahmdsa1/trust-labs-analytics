"""
Trust Labs Data Pipeline - Data Loader
"""

import pandas as pd
import os
import glob
import logging
import config

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


class DataLoader:
    
    def __init__(self):
        self.data_folder = config.DATA_FOLDER
        self.stats = {'files_found': 0, 'files_loaded': 0, 'total_records': 0}
    
    def find_csv_files(self, filename):
        pattern = os.path.join(self.data_folder, '**', filename)
        files = glob.glob(pattern, recursive=True)
        self.stats['files_found'] = len(files)
        logger.info(f"Found {len(files)} files: {filename}")
        return files
    
    def load_csv(self, filepath):
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            logger.info(f"✅ Loaded {len(df)} records from {os.path.basename(filepath)}")
            self.stats['files_loaded'] += 1
            self.stats['total_records'] += len(df)
            return df
        except Exception as e:
            logger.error(f"❌ Error loading {filepath}: {e}")
            return None
    
    def extract_branch_name(self, filepath):
        folder = os.path.basename(os.path.dirname(filepath))
        branch = folder.replace('Branch_', '')
        import re
        branch = re.sub(r'^\d+_', '', branch)
        branch = branch.replace('_', ' ')
        return branch
    
    def load_all_patient_visits(self):
        logger.info("\n" + "="*60)
        logger.info("LOADING PATIENT VISITS")
        logger.info("="*60)
        
        files = self.find_csv_files('patient_visits.csv')
        
        if not files:
            logger.warning("No patient_visits.csv found!")
            return pd.DataFrame()
        
        all_data = []
        for filepath in files:
            df = self.load_csv(filepath)
            if df is not None:
                all_data.append(df)
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            logger.info(f"✅ TOTAL VISITS: {len(combined)}")
            return combined
        
        return pd.DataFrame()
    
    def extract_unique_patients(self, visits_df):
        logger.info("\n" + "="*60)
        logger.info("EXTRACTING PATIENTS")
        logger.info("="*60)
        
        if visits_df.empty:
            return pd.DataFrame()
        
        # Use actual column names from config
        patient_cols = config.PATIENT_COLUMNS
        
        # Only keep columns that exist in the dataframe
        existing_cols = [c for c in patient_cols if c in visits_df.columns]
        
        # Get unique patients (first occurrence of each Patient_ID)
        patients = visits_df[existing_cols].drop_duplicates(subset=['Patient_ID'], keep='first')
        
        logger.info(f"✅ PATIENTS: {len(patients)}")
        return patients
    
    def print_summary(self):
        logger.info("\n" + "="*60)
        logger.info("LOADING SUMMARY")
        logger.info("="*60)
        logger.info(f"Files found: {self.stats['files_found']}")
        logger.info(f"Files loaded: {self.stats['files_loaded']}")
        logger.info(f"Total records: {self.stats['total_records']}")