# Simple code to peek at the csv

# Imports
from pathlib import Path
import polars as pl
import pandas as pd

# Constants (settings, paths etc)
CSV_NAME = "selling_overview" # with or without .csv
CSV_FOLDER_PATH = (
    Path(__file__).parent /
    "01_dataset_from_html" / "results"
)

# Script

final_path = (CSV_FOLDER_PATH / CSV_NAME).with_suffix(".csv")
print("Opening:", final_path)
print("File exists:", final_path.is_file())
peek_df = pl.read_csv(final_path, glob=False)
print("CSV opened.")
print(peek_df)
#print("CSV head:")
#print(peek_df.head())
print("CSV columns:")
print(peek_df.columns)
