import os
import numpy as np
import pandas as pd

from src.data.etl._utils import get_raw_dataset_name_from_filename, create_interim_filename_from_dataset_name, generate_full_csv_filename
from src.utils.constants import get_folders_constants, get_scraping_constants




def build_interim_datasets():
    RAW_CSVS_BASE_PATH = get_folders_constants()['RAW_CSV_BASE_FILEPATH']

    all_files_in_folder = [
        os.path.join(RAW_CSVS_BASE_PATH, file)
        for file in os.listdir(RAW_CSVS_BASE_PATH)
    ]

    all_csv_files = list(filter(
        lambda filename: filename.endswith('csv'),
        all_files_in_folder
    ))

    all_dataframes = {}

    for full_path_filename in all_csv_files:
        FILENAME = full_path_filename.split(os.sep)[-1]
        print(f"---- STARTS BASIC PROCESSING {FILENAME} ----")
        dataset_name = get_raw_dataset_name_from_filename(full_path_filename)

        print("Applying base transformations to dataset",
              full_path_filename.split(os.sep)[-1])
        transformed_df = _apply_common_transformations_to_dataset(
            pd.read_csv(full_path_filename)
        )
        print("SUCCESS")

        print(f"Storing dataset {dataset_name}")
        all_dataframes[dataset_name] = transformed_df
        print("SUCCESS")
        print(f"---- ENDS BASIC PROCESSING {FILENAME} ----")

    advanced_df_key = list(filter(lambda df_name: df_name.startswith(
        'advanced'), all_dataframes.keys()))[0]

    for dataset_name in all_dataframes.keys():
        print(f"---- STARTS PROCESSING {FILENAME} ----")
        print(f"ADDING WINS, LOSSES BY SEASON {dataset_name} dataset")
        if 'advanced' in dataset_name:
            continue
        else:
            all_dataframes[dataset_name] = _add_wins_losses_by_season(
                all_dataframes[dataset_name], all_dataframes[advanced_df_key])
        print(f"---- ENDS PROCESSING {FILENAME} ----")

    print("SUCCESS")
    for dataset_name, dataframe in all_dataframes.items():
        filename = create_interim_filename_from_dataset_name(dataset_name)
        FILENAME = filename.split(os.sep)[-1]
        print(f"---- SAVING FILE INTO {FILENAME} ----")
        print(f"STORING {dataset_name} in {filename}")
        dataframe.to_csv(filename, index=False)
        print("---- SUCCESS ----")
