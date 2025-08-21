# The first scraping script for selling data

# Imports
import os
from bs4 import BeautifulSoup, NavigableString
import re
import pandas as pd
from my_utils import price_int_from_str

# Constants (settings, paths etc)
SELLING_HTML_FILE_PATH = os.path.join(
    "01_data_prep/shop_html/",
    "Toko  Online - Produk Lengkap & Harga Terbaik ｜ Tokopedia (8_21_2025 10：58：57 AM)"
    + ".html"
)
CSV_RESULT_NAME_NO_EXT = "selling_overview" # without .csv
CSV_RESULT_FOLDER_PATH = "01_data_prep/results/"

# Script

with open(SELLING_HTML_FILE_PATH, "r") as file:
    html_text = file.read()

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
        title_list.append(cur_title)
        author_list.append(cur_author)
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

new_df = pd.DataFrame(results_dict)

final_path = os.path.join(
    CSV_RESULT_FOLDER_PATH,
    CSV_RESULT_NAME_NO_EXT + ".csv"
)
print("Saving to:")
print(final_path)
new_df.to_csv(final_path, index=False)
print("Saved")
