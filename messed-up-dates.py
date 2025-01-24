import pandas as pd
import re

data = pd.read_csv("date_watched.csv")

def clean_datetime(series):
    # Remove specific prefixes (like 'Crgpug')
    cleaned = series.str.replace(r'^.*?(?=\w{3} \d{1,2})', '', regex=True)
    
    # Remove 'WAT' and strip any extra whitespace
    cleaned = cleaned.str.strip().str.replace(' WAT', '')
    
    return pd.to_datetime(cleaned, format='%b %d, %Y, %I:%M:%S %p')



data['date_watched'] = clean_datetime(data['date_watched'])
print(data['date_watched'])

