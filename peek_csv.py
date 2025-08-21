# Simple code to peek at the csv

# Imports
import pandas as pd

# Constants (settings, paths etc)
CSV_NAME_NO_EXT = "selling_overview" # without .csv
CSV_FOLDER_PATH = "01_data_prep/results"

# Script

final_path = CSV_FOLDER_PATH + "/" + CSV_NAME_NO_EXT + ".csv"
print("Opening:", final_path)
peek_df = pd.read_csv(final_path)
print("CSV opened.")
print("CSV head:")
print(peek_df.head())
print("CSV desc:")
peek_df.info()
print("CSV columns:")
print(peek_df.columns)
