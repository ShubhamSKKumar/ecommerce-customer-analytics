import os

# Centralized configuration for the analytics pipeline
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')
DB_PATH = os.path.join(BASE_DIR, 'ecommerce.db')

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

# File paths
RAW_CSV_PATH = os.path.join(RAW_DATA_DIR, 'online_retail.csv')
CLEANED_CSV_PATH = os.path.join(CLEANED_DATA_DIR, 'online_retail_cleaned.csv')
FEATURES_CSV_PATH = os.path.join(CLEANED_DATA_DIR, 'online_retail_features.csv')
SEGMENTS_CSV_PATH = os.path.join(CLEANED_DATA_DIR, 'customer_segments.csv')
