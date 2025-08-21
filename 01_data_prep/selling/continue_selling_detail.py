# The second scraping script for selilng data,
# to be run after the first (start_selling_overview)

# Imports
from bs4 import BeautifulSoup
import pandas as pd

# Constants (settings, paths etc)
SELLING_HTML_PATH = (
    "01_data_prep/shop_html/"
    + "Toko  Online - Produk Lengkap & Harga Terbaik ｜ Tokopedia (8_21_2025 10：58：57 AM)"
    + ".html"
)
OVERVIEW_RESULT_NAME_NO_EXT = "selling_overview" # without .csv
DETAIL_RESULT_NAME_NO_EXT = "selling_detail"
CSV_RESULT_FOLDER_PATH = "01_data_prep/results"

# Script

overview_path = (
    CSV_RESULT_FOLDER_PATH + "/" + OVERVIEW_RESULT_NAME_NO_EXT
    + ".csv"
)
overview_df = pd.read_csv(overview_path)
overview_cols = overview_df.columns
overview_rowlen = len(overview_df)

if ("title_author" in overview_cols):
    title_author_list = list(overview_df["title_author"])
elif (("title" in overview_cols) and
      ("author" in overview_cols)):
    title_list = list(overview_df["title"])
    author_list = list(overview_df["author"])
    title_author_list = [
        title_list[i] + " - " + author_list[i]
        for i in range(overview_rowlen)
    ]
    print(title_author_list)
else:
    print("Error: cannot identify title and/or author column(s)")
    title_author_list = None # expect errors from this point on

# to be done
