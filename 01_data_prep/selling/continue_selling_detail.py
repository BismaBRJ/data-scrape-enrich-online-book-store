# The second scraping script for selilng data,
# to be run after the first (start_selling_overview)

# Imports
import os
import pandas as pd
import re
from bs4 import BeautifulSoup

# Constants (settings, paths etc)
SELLING_HTML_FOLDER_PATH = "01_data_prep/shop_html/"
OVERVIEW_RESULT_NAME_NO_EXT = "selling_overview" # without .csv
DETAIL_RESULT_NAME_NO_EXT = "selling_detail"
CSV_RESULT_FOLDER_PATH = "01_data_prep/results/"

# Script

overview_path = os.path.join(
    CSV_RESULT_FOLDER_PATH,
    OVERVIEW_RESULT_NAME_NO_EXT + ".csv"
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
        title + " - " + author
        for title, author in zip(title_list, author_list)
    ]
else:
    print("Error: cannot identify title and/or author column(s)")
    title_author_list = None # expect errors from this point on

detail_df = overview_df.copy()
html_file_names = [
    filename
    for filename in os.listdir(SELLING_HTML_FOLDER_PATH)
    if os.path.isfile(
        os.path.join(SELLING_HTML_FOLDER_PATH, filename)
    )
]
html_file_paths = [
    os.path.join(SELLING_HTML_FOLDER_PATH, filename)
    for filename in html_file_names
]

for title_author in title_author_list:
    title_author_re = re.compile(title_author)
    cur_title_author = list(filter(title_author_re.search, html_file_paths))

# to be done
