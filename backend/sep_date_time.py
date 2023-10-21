import pandas as pd
from datetime import datetime

# read csv
file_path = ".\\csvData\\2023MCH_EmpEntry.csv"
df = pd.read_csv(file_path)

df['DateTime'] = pd.to_datetime(df['DateTime'])

df['Date'] = df['DateTime'].dt.date
df['Time'] = df['DateTime'].dt.time

df = df.drop(columns='DateTime')

df.to_csv(".\\csvData\\sep_date_time.csv", index=False)