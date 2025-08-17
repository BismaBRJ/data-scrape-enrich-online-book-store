# This script renames all files in a folder to replace a certain keyword

# Imports
import os
import re

# Constants
FOLDER_PATH = "01_data_prep/shop_html"
OLD_KEYWORD = "(store name)" # was once the store name
NEW_KEYWORD = ""

# Script

all_files_folders = os.listdir(FOLDER_PATH)
old_files = [
    x
    for x in all_files_folders
    if os.path.isfile(os.path.join(FOLDER_PATH, x))
]

old_pattern = re.compile(OLD_KEYWORD)

for old_name in old_files:
    new_name = re.sub(old_pattern, NEW_KEYWORD, old_name)

    old_path = os.path.join(FOLDER_PATH, old_name)
    new_path = os.path.join(FOLDER_PATH, new_name)
    os.rename(old_path, new_path)
