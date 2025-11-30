import pandas as pd
import re
import numpy as np
from datetime import datetime, timedelta
import random
import io

def clean_social_media_data(input_file, output_file):
    print("🧹 Starting data cleaning process...")

    # 1. Read the raw file content as a string first to handle the text issues
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'. Please check the file name.")
        return

    # 2. Text Cleaning using Regex

    content_no_citations = re.sub(r'\'\'', '', raw_content)
    
    content_fixed_lines = re.sub(r'Live \n\s*Stream', 'Live Stream', content_no_citations)

    try:
        df = pd.read_csv(io.StringIO(content_fixed_lines))
    except Exception as e:
        print(f"❌ Error parsing CSV data: {e}")
        return

    numeric_cols = ['Views', 'Likes', 'Shares', 'Comments']
    for col in numeric_cols:

        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    print("📅 Generating synthetic dates for dashboard compatibility...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    random_days = np.random.randint(0, 365, size=len(df))
    df['Post_Date'] = [start_date + timedelta(days=int(day)) for day in random_days]
    
    df['Post_Date'] = df['Post_Date'].dt.date


    try:
        df.to_csv(output_file, index=False)
        print(f"✅ Success! Cleaned data saved to: {output_file}")
        print(f"📊 Total Records Processed: {len(df)}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

# --- Execution ---
if __name__ == "__main__":
    INPUT_FILENAME = 'Viral_Social_Media_Trends.csv'
    OUTPUT_FILENAME = 'Cleaned_Viral_Social_Media_Trends.csv'
    
    clean_social_media_data(INPUT_FILENAME, OUTPUT_FILENAME)