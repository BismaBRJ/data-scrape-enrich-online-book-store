# The first scraping script for review data

# Imports
from pathlib import Path
from bs4 import BeautifulSoup

# Constants (settings, paths etc)
REVIEWS_HTML_FOLDER_PATH = Path(__file__).parent.parent / "shop_html"
REVIEWS_HTML_FILE_NAMES = [ # with or without .html
    "reviews01 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：43：47 PM)",
    "reviews02 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：44：06 PM)",
    "reviews03 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：44：25 PM)"
]
CSV_RESULT_NAME = "reviews_overview" # with or without .csv
CSV_RESULT_FOLDER_PATH = Path(__file__).parent.parent / "results"

# Script

for html_name in REVIEWS_HTML_FILE_NAMES:
    html_path = (REVIEWS_HTML_FOLDER_PATH / html_name).with_suffix(".html")
    pass

# to be done
