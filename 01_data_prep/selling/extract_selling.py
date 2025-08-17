# Imports
from bs4 import BeautifulSoup, NavigableString
import re
import pandas as pd

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

# [...] Rp [???].[?]00 [...]
contains_price_re = re.compile("(.*?)Rp([0-9.,\s]*)00(.*)")

price_descs_raw = soup.find_all("div", string=contains_price_re)

# only taking the strings (not tags containing them) to prevent duplication
price_navstrs = [
    descendant
    for descendant in price_descs_raw
    if (type(descendant) == NavigableString)
]

# possibly it is not the strings themselves that were found,
# rather the tags containing the strings
if len(price_navstrs) == 0:
    price_tags = [ # doesn't have yet another div inside
        tag
        for tag in price_descs_raw
        if
            (len(tag.contents) == 1) and
            (type(tag.contents[0]) == NavigableString)
    ]
else: # in case the strings themselves were found already
    # for uniformity, store the parent tags instead of the navstrings
    price_tags = [
        navstr.parent
        for navstr in price_navstrs
    ]

def debug_price_tags():
    print("print(len(price_tags)):")
    print(len(price_tags))
    print("=" * 10)

    print("print(price_tags):")
    print(price_tags)
    print("=" * 10)

    print("print(print(price_tags[0])):")
    print(price_tags[0])
    print("=" * 10)

    print("print(price_tags[0].parent):")
    print(price_tags[0].parent)
    print("=" * 10)

    print("print(price_tags[0].parent.parent):")
    print(price_tags[0].parent.parent)
    print("=" * 10)

#debug_price_tags()

# to be done
