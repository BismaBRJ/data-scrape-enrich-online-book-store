# The first scraping script for review data

# Imports
from pathlib import Path
from bs4 import BeautifulSoup
import re
import polars as pl

# Constants (settings, paths etc)
REMOVE_UNSEPARABLE = True
REVIEWS_HTML_FOLDER_PATH = Path(__file__).parent.parent / "shop_html"
REVIEWS_HTML_FILE_NAMES = [ # with or without .html
    "reviews01 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：43：47 PM)",
    "reviews02 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：44：06 PM)",
    "reviews03 Toko  Online - Produk Lengkap & Harga Terbaik (8_13_2025 11：44：25 PM)"
]
CSV_RESULT_NAME = "reviews_sep_overview" # with or without .csv
CSV_RESULT_FOLDER_PATH = Path(__file__).parent.parent / "results"

# Script

title_author_list = []
title_list = []
author_list = []
title_author_separable = True # assume true until proven false
rating_list = []
review_txt_list = []
thumb_base64_list = []
review_imgs_base64_list = []

review_re = re.compile("(.*)review(.*)")

for html_name in REVIEWS_HTML_FILE_NAMES:
    html_path = (REVIEWS_HTML_FOLDER_PATH / html_name).with_suffix(".html")
    html_text = html_path.read_text()
    soup = BeautifulSoup(html_text, "html.parser")
    
    product_link_tags = soup.find_all("a", attrs={"class": "styProduct"})
    #print("len(product_link_tags) =", len(product_link_tags))
    #print(product_link_tags[0])
    for product_link_tag in product_link_tags:
        title_author_tag = product_link_tag.find("p")
        cur_title_author = title_author_tag.text

        cur_title_author_list = cur_title_author.split(" - ")
        if (len(cur_title_author_list) == 2):
            cur_title, cur_author = cur_title_author_list
            equal_space_title = re.sub(r"\s+", " ", cur_title)
            equal_space_author = re.sub(r"\s+", " ", cur_author)
            title_list.append(equal_space_title.rstrip())
            author_list.append(equal_space_author.lstrip())
        elif REMOVE_UNSEPARABLE:
            continue # skip this row
        elif title_author_separable:
            title_author_separable = False

        title_author_list.append(cur_title_author)
        product_link_tag.find("span").decompose()
        # there is an irrelevant image in there

        thumb_base64_tag = product_link_tag.find("img")
        cur_thumb_base64 = thumb_base64_tag["src"]
        thumb_base64_list.append(cur_thumb_base64)

        overall_product_tag = product_link_tag.parent
        product_link_tag.decompose() # no longer needed
        product_review_tag = overall_product_tag.find("div") # outermost

        stars_tag = product_review_tag.find(
            "div",
            attrs={"data-testid": "icnStarRating"}
        )
        cur_rating = len(tuple(stars_tag.children)) # how many star images
        rating_list.append(cur_rating)
        stars_tag.parent.parent.decompose() # heavily nested & no longer needed

        review_txt_tag = product_review_tag.find("p").find("span")
        cur_review_txt = review_txt_tag.text
        review_txt_list.append(cur_review_txt)
        review_txt_tag.parent.decompose()

        product_review_tag.find(
            "span", attrs={"class": "name"} # username
        ).parent.decompose()

        review_imgs_base64_tags = product_review_tag.find_all(
            "img", attrs={"alt": review_re}
        )
        cur_review_imgs_base64 = [
            img_tag["src"]
            for img_tag in review_imgs_base64_tags
        ]
        review_imgs_base64_list.append(cur_review_imgs_base64)

review_imgs_base64_str_list = map(str, review_imgs_base64_list)

if title_author_separable:
    results_dict = {
        "title": title_list,
        "author": author_list,
        "rating": rating_list,
        "review_txt": review_txt_list,
        "thumb_base64": thumb_base64_list,
        "review_imgs_base64": review_imgs_base64_str_list
    }
else:
    results_dict = {
        "title_author": title_author_list,
        "rating": rating_list,
        "review_txt": review_txt_list,
        "thumb_base64": thumb_base64_list,
        "review_imgs_base64": review_imgs_base64_str_list
    }

new_df = pl.DataFrame(results_dict)

final_path = (
    CSV_RESULT_FOLDER_PATH / CSV_RESULT_NAME
).with_suffix(".csv")
print("Saving to:")
print(final_path)
new_df.write_csv(final_path)
print("Saved")
