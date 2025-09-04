
# Imports
from torch.utils.data import Dataset
from pathlib import Path
import polars as pl

# Code

class TitleAuthorEmbeddingDataset(Dataset):
    def __init__(self):
        super().__init__()
