# The second scraping script for review data,
# to be run after the first (start_reviews_overview)

# Imports
from pathlib import Path
import polars as pl
import re
from bs4 import BeautifulSoup
from utils_prep_reviews import price_int_from_str

# Constants (settings, paths etc)
WITH_SLIDERS_IMG = True
SELLING_HTML_FOLDER_PATH = Path(__file__).parent.parent / "shop_html"
OVERVIEW_RESULT_NAME = "reviews_overview" # with or without .csv
DETAIL_RESULT_NAME = "reviews_detail"
CSV_RESULT_FOLDER_PATH = Path(__file__).parent.parent / "results"

# Script

overview_path = (
    CSV_RESULT_FOLDER_PATH / OVERVIEW_RESULT_NAME
).with_suffix(".csv")
overview_df = pl.read_csv(overview_path, glob=False)
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

html_file_paths = []
for full_file_path in SELLING_HTML_FOLDER_PATH.iterdir():
    if full_file_path.is_file():
        html_file_paths.append(full_file_path)

price_list = []
desc_list = []
if WITH_SLIDERS_IMG:
    sliders_base64_list = []

for title_author in title_author_list:
    match_html_file_paths = [
        html_file_path
        for html_file_path in html_file_paths
        if  (
                (title_author in html_file_path.name)
                or
                (
                    title_author.replace(":", "：")
                    # special character since : is not
                    # allowed for file names on macOS
                    in html_file_path.name
                )
                or
                (
                    title_author.replace(":", "：").replace("*", "＊")
                    # similar situation for the asterisk I guess
                    in html_file_path.name
                )
            )
    ]
    num_matches = len(match_html_file_paths)
    if (num_matches == 1):
        cur_html_file_path = match_html_file_paths[0]
    elif (num_matches == 0):
        print("Error: HTML file not found for title_author:", title_author)
        cur_html_file_path = None
    else:
        print("Error: Multiple HTML files for title_author:", title_author)
        print("They are:", match_html_file_paths)
        print("Selecting first one...")
        cur_html_file_path = match_html_file_paths[0]
    
    cur_html_text = cur_html_file_path.read_text()
    cur_soup = BeautifulSoup(cur_html_text, "html.parser")

    cur_price_tag = cur_soup.find(
        "div",
        attrs = {"data-testid": "lblPDPDetailProductPrice"}
    )
    cur_price = price_int_from_str(cur_price_tag.text)
    price_list.append(cur_price)

    cur_desc_tag = cur_soup.find(
        "div",
        attrs = {"data-testid": "lblPDPDescriptionProduk"}
    )
    cur_desc = cur_desc_tag.text
    desc_list.append(cur_desc)

    if not WITH_SLIDERS_IMG:
        continue
    
    cur_imgs_base64_list = []
    cur_imgs_parent_tag = cur_soup.find(
        "div",
        attrs = {"data-testid": "listPDPSlider"}
    )
    cur_imgs_parent_tag_children = list(cur_imgs_parent_tag.children)
    nonempty_alt_re = re.compile(r".+?")
    if (len(cur_imgs_parent_tag_children) == 1):
        cur_imgs_tag = cur_imgs_parent_tag_children[0]
        for img_parent_tag in cur_imgs_tag.children:
            img_tag = img_parent_tag.find(
                "img",
                attrs = {"alt": nonempty_alt_re}
            )
            cur_imgs_base64_list.append(img_tag["src"])
    
    sliders_base64_list.append(tuple(cur_imgs_base64_list))

rating_col_idx = overview_cols.index("rating")
detail_cols = (
    overview_cols[:rating_col_idx] +
    ["price", "desc"] +
    overview_cols[rating_col_idx:]
)
detail_df = overview_df.with_columns(
    pl.Series("price", price_list),
    pl.Series("desc", desc_list)
)
detail_df = detail_df.select(detail_cols)

if WITH_SLIDERS_IMG:
    detail_cols = (
        detail_cols[:-1] +
        ["sliders_base64"] +
        [detail_cols[-1]]
    )
    detail_df = detail_df.with_columns(
        pl.Series(
            "sliders_base64",
            map(str, sliders_base64_list)
        )
    )
    detail_df = detail_df.select(detail_cols)

detail_path = (
    CSV_RESULT_FOLDER_PATH / DETAIL_RESULT_NAME
).with_suffix(".csv")
print("Saving to:")
print(detail_path)
detail_df.write_csv(detail_path)
print("Saved")
