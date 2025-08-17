# Imports
from bs4 import BeautifulSoup

# Constants (paths etc)
SELLING_HTML_PATH = (
    "01_data_prep/shop_html/" +
    "Toko  Online - Produk Lengkap & Harga Terbaik ｜ Tokopedia (8_13_2025 11：43：25 PM)" +
    ".html"
)

# Script

with open(SELLING_HTML_PATH, "r") as file:
    html_text = file.read()

soup = BeautifulSoup(html_text, "html.parser")

# to be done
