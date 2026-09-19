import os
import urllib.request
import zipfile
import pandas as pd
import warnings

# Suppress openpyxl warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

from src import config

def download_and_extract_data():
    url = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
    zip_path = os.path.join(config.RAW_DATA_DIR, "online_retail.zip")
    extracted_dir = os.path.join(config.RAW_DATA_DIR, "extracted")
    csv_path = config.RAW_CSV_PATH

    # Create directories if they don't exist
    os.makedirs(config.RAW_DATA_DIR, exist_ok=True)
    os.makedirs(extracted_dir, exist_ok=True)

    if os.path.exists(csv_path):
        print(f"{csv_path} already exists. Skipping download.")
        return

    print("Downloading dataset from UCI Machine Learning Repository...")
    urllib.request.urlretrieve(url, zip_path)

    print("Extracting zip file...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extracted_dir)

    # Find the excel file in the extracted directory
    excel_file = None
    for file in os.listdir(extracted_dir):
        if file.endswith(".xlsx"):
            excel_file = os.path.join(extracted_dir, file)
            break

    if not excel_file:
        print("Error: Could not find the Excel file in the extracted dataset.")
        return

    print(f"Loading Excel file: {excel_file} (This may take a minute...)")
    df = pd.read_excel(excel_file)

    print(f"Saving to CSV: {csv_path}")
    df.to_csv(csv_path, index=False)

    print(f"Dataset successfully downloaded and saved to {csv_path}!")
    print(f"Total records: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    download_and_extract_data()
