import os
import pandas as pd

from src.utils.files import generate_full_csv_filename
from src.utils.constants import get_folders_constants


def create_totals_raw_datasets() -> None:
    scraped_data_csv_folders_path = get_folders_constants()[
        'EXTERNAL_CSV_BASE_FILEPATH']

    scraped_data_csv_folders_csv_folders = list(filter(
        lambda filename: filename.endswith('stats'), os.listdir(scraped_data_csv_folders_path))
    )

    for folder in scraped_data_csv_folders_csv_folders:
        print("------------------------------------------------------------")
        print(f"Creating full dataset for {folder} folder")

        folder_csv_files_path = os.path.join(
            scraped_data_csv_folders_path, folder)

        folder_csv_filenames = [
            os.path.join(folder_csv_files_path, filename) for filename in os.listdir(folder_csv_files_path)
        ]

        print(f"Reading {len(folder_csv_filenames)} datasets.")
        print(f"Merging {len(folder_csv_filenames)} datasets into one")

        raw_full_dataset = pd.concat([
            pd.read_csv(csv_file) for csv_file in folder_csv_filenames
        ])

        raw_full_dataset_filepath = generate_full_csv_filename(
            f'{folder}_full_dataset', 'raw')

        print(f"Saving full dataset in {raw_full_dataset_filepath}")

        raw_full_dataset.to_csv(raw_full_dataset_filepath, index=False)

        print("Success!")
