import os
from shutil import rmtree
from typing import List


def remove_files(files: List[str]) -> None:
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
            print(f'{file} has been removed')
        elif os.path.isdir(file):
            rmtree(file)
            print(f'{file} has been removed')
