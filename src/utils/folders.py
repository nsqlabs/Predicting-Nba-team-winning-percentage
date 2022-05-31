import os
from pathlib import Path
from typing import List


def get_root_folder():
    return Path(__file__).parents[2]


def list_folder_content(path: str) -> List[str]:
    return os.listdir(path)
