# The first scraping script for selling data

# Imports
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re
import polars as pl
from utils_prep_selling import price_int_from_str

# Constants (settings, paths etc)
SELLING_HTML_FILE_PATH = (
    Path(__file__).parent.parent / "shop_html" /
    "Toko  Online - Produk Lengkap & Harga Terbaik ｜ Tokopedia (8_21_2025 10：58：57 AM)"
).with_suffix(".html")
CSV_RESULT_NAME = "selling_overview" # with or without .csv
CSV_RESULT_FOLDER_PATH = Path(__file__).parent.parent / "results"

# Script

html_text = SELLING_HTML_FILE_PATH.read_text()
soup = BeautifulSoup(html_text, "html.parser")

# Plan:
# 1. Get all the tags of the prices (easy search by regex)
# 2. Climb up to parent to get other data, like item name

# [...] Rp [???].[?]00 [...]
contains_price_re = re.compile(r"(.*?)Rp([0-9.,\s]*)00(.*)")

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

def debug_price_tags(price_tags, price_to_int=True):
    print("print(len(price_tags)):")
    print(len(price_tags))
    print("=" * 10)

    print("print(price_tags):")
    print(price_tags)
    print("=" * 10)

    print("print(print(price_tags[0])):")
    print(price_tags[0])
    print("=" * 10)

    print("print(price_tags[0].text):")
    print(price_tags[0].text)
    print("=" * 10)

    if price_to_int:
        print("print(price_int_from_str(price_tags[0].text))")
        print(price_int_from_str(price_tags[0].text))
        print("=" * 10)

    print("print(price_tags[0].parent):")
    print(price_tags[0].parent)
    print("=" * 10)

    print("print(price_tags[0].parent.parent):")
    print(price_tags[0].parent.parent)
    print("=" * 10)

    print("print(price_tags[0].parent.parent.parent):")
    print(price_tags[0].parent.parent.parent)
    print("=" * 10)

#debug_price_tags(price_tags)

# The Title - Lastname & Lastname
is_title_author_re = re.compile(r".*? - [^-]*")

#print(re.search(is_title_author_re, "aaa - bbb - ccc"))

title_author_list = []
title_list = []
author_list = []
title_author_separable = True # assume true until proven false
price_list = []
thumb_base64_list = []

for price_tag in price_tags:
    cur_price = price_int_from_str(price_tag.text)
    price_list.append(cur_price)

    parent_with_title = price_tag.parent.parent
    cur_title_author_tag = parent_with_title.find(
        "span",
        string=is_title_author_re
    )
    cur_title_author = cur_title_author_tag.text
    title_author_list.append(cur_title_author)

    cur_title_author_list = cur_title_author.split(" - ")
    if (len(cur_title_author_list) == 2):
        cur_title, cur_author = cur_title_author_list
        equal_space_title = re.sub(r"\s+", " ", cur_title)
        equal_space_author = re.sub(r"\s+", " ", cur_author)
        title_list.append(equal_space_title.rstrip())
        author_list.append(equal_space_author.lstrip())
    elif title_author_separable:
        title_author_separable = False

    parent_with_thumb = parent_with_title.parent
    parent_with_title.decompose()
    # Delete that entire tag. Why?
    # 1. We're done with it, and
    # 2. it has some misleading, irrelevant image file
    cur_thumb_tag = parent_with_thumb.find("img") # only one image now
    cur_thumb_data = cur_thumb_tag["src"]
    thumb_base64_list.append(cur_thumb_data)

if title_author_separable:
    results_dict = {
        "title": title_list,
        "author": author_list,
        "price": price_list,
        "thumb_base64": thumb_base64_list
    }
else:
    results_dict = {
        "title_author": title_author_list,
        "price": price_list,
        "thumb_base64": thumb_base64_list
    }

new_df = pl.DataFrame(results_dict)

final_path = (
    CSV_RESULT_FOLDER_PATH / CSV_RESULT_NAME
).with_suffix(".csv")
print("Saving to:")
print(final_path)
new_df.write_csv(final_path)
print("Saved")
