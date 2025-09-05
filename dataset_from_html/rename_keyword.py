# This script renames all files in a folder to replace a certain keyword

# Imports
from pathlib import Path
import re

# Constants
FOLDER_PATH = Path(__file__).parent / "shop_html"
OLD_KEYWORD = "Store Name" # was once the store name
NEW_KEYWORD = ""

# Script

all_files_folders = FOLDER_PATH.iterdir()
old_names = [
    old_path.name
    for old_path in all_files_folders
    if old_path.is_file()
]

old_pattern = re.compile(OLD_KEYWORD)

for old_name in old_names:
    new_name = re.sub(old_pattern, NEW_KEYWORD, old_name)

    old_path = FOLDER_PATH / old_name
    new_path = FOLDER_PATH / new_name
    old_path.rename(new_path)
