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

price_tags_raw = soup.find_all("div", string=contains_price_re)

price_tags_navstr = [ # strings only
    tag
    for tag in price_tags_raw
    if (type(tag) == NavigableString)
]

# possibly it is not the strings themselves that are found,
# rather the tags containing the strings
if len(price_tags_navstr) == 0:
    price_tags = [ # doesn't have yet another div inside
        tag
        for tag in price_tags_raw
        if
            (len(tag.contents) == 1) and
            (type(tag.contents[0]) == NavigableString)
    ]
else: # in case the strings themselves were found already
    price_tags = price_tags_navstr
    # shallow copy is fine, just renaming variables anyway

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

debug_price_tags()

# to be done
