"""
Trust Labs Data Pipeline - Data Cleaner
"""

import pandas as pd
from datetime import datetime
import logging
import config

logger = logging.getLogger(__name__)


class DataCleaner:
    
    def __init__(self):
        self.stats = {
            'total_records': 0,
            'duplicates_removed': 0,
            'cleaned_records': 0
        }
    
    def clean_date(self, date_value):
        if pd.isna(date_value):
            return None
        
        try:
            if isinstance(date_value, str):
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(date_value, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            elif isinstance(date_value, (datetime, pd.Timestamp)):
                return date_value.strftime('%Y-%m-%d')
            return str(date_value)
        except Exception as e:
            logger.warning(f"Could not parse date: {date_value}")
            return None
    
    def remove_duplicates(self, df, columns):
        initial = len(df)
        df = df.drop_duplicates(subset=columns, keep='first')
        removed = initial - len(df)
        self.stats['duplicates_removed'] += removed
        if removed > 0:
            logger.info(f"Removed {removed} duplicates")
        return df
    
    def clean_patients(self, df):
        logger.info(f"Cleaning {len(df)} patient records...")
        self.stats['total_records'] += len(df)
        
        # Remove rows with missing Patient_ID
        df = df[df['Patient_ID'].notna()]
        
        # Standardize Gender
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].str.strip().str.title()
        
        # Remove duplicates by Patient_ID
        df = self.remove_duplicates(df, [config.PATIENT_UNIQUE_KEY])
        
        # Fill missing values
        df = df.fillna('')
        
        self.stats['cleaned_records'] += len(df)
        logger.info(f"✅ Cleaned {len(df)} patients")
        return df
    
    def clean_visits(self, df):
        logger.info(f"Cleaning {len(df)} visit records...")
        self.stats['total_records'] += len(df)
        
        # Remove rows with missing Patient_ID
        df = df[df['Patient_ID'].notna()]
        
        # Clean visit date
        if 'Visit_Date' in df.columns:
            df['Visit_Date'] = df['Visit_Date'].apply(self.clean_date)
        
        # Remove duplicates
        df = self.remove_duplicates(df, config.VISIT_UNIQUE_KEYS)
        
        # Fill missing values
        df = df.fillna('')
        
        self.stats['cleaned_records'] += len(df)
        logger.info(f"✅ Cleaned {len(df)} visits")
        return df