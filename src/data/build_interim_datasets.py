from typing import final

from pyparsing import Optional
from src.utils.constants import get_folders_constants, get_scraping_constants
from src.utils.folders import get_root_folder
import os
import numpy as np
import pandas as pd


def add_season_to_dataframe(team_series):
    FINAL_YEAR = get_scraping_constants()['LAST_YEAR']
    INITIAL_YEAR = FINAL_YEAR - get_scraping_constants()['N_PREVIOUS_YEARS']
    current_year = INITIAL_YEAR

    def get_season_year(team_name):
        nonlocal current_year
        if team_name == 'League Average':
            current_year += 1
            return 0
        return current_year

    get_season_year_vectorized = np.vectorize(get_season_year)
    return get_season_year_vectorized(team_series)


def delete_first_unnamed_columns(stats_df):
    columns_to_delete = []
    for column in stats_df.columns:
        if column.startswith('Unnamed'):
            columns_to_delete.append(column)
        else:
            break
    return stats_df.drop(columns_to_delete, axis=1)


def apply_common_transformations_to_dataset(stats_df: pd.DataFrame) -> pd.DataFrame:
    final_df = stats_df.copy()

    # Removing first columns with the Unnamed pattern
    final_df = delete_first_unnamed_columns(final_df)

    # Adding season prop to the dataset
    final_df['Season'] = add_season_to_dataframe(final_df.Team)

    # Removing league average summary row
    final_df = final_df.drop(
        final_df[final_df['Season'] == 0].index
    ).reset_index(drop=True)

    # Add a playoffs classification column
    final_df['Playoffs'] = (final_df['Team'].str.endswith('*')).astype(int)

    # Dropping the Rk column (it's not related to final positions but to order in table)
    final_df = final_df.drop('Rk', axis=1)

    # Ordering by season, playoffs classification, and team
    final_df = final_df.sort_values(
        by=["Season", "Playoffs", "Team"],
        ascending=[False, False, True]
    ).reset_index(drop=True)
    
    # Remove * from name
    final_df['Team'] = final_df['Team'].apply(lambda x: x.replace('*', ''))

    return final_df


def add_wins_losses_by_season(stats_df, advanced_stats_df):
    print(stats_df.columns)

    stats_df_copy = stats_df.copy()  # copy input df
    stats_df_copy.loc[:, ['W', 'L']] = advanced_stats_df.loc[:, [
        'W', 'L']].copy()  # extract wins and losses column
    stats_df_copy = stats_df_copy.sort_values(
        by=["Season", "W", "Playoffs"],
        ascending=[False, False, True]
    )
    return stats_df_copy.reset_index(drop=True)


def get_dataset_name_from_filename(filename):
    return f"{filename.split(os.sep)[-1].split('_raw_')[0]}_interim_df"


def get_filename_from_dataset_name(dataset_name):
    # remove _df and append .csv
    csv_filename = f"{dataset_name.split('_df')[0]}.csv"
    print(csv_filename)
    dataset_interim_folder_save_path = os.path.join(
        get_folders_constants()['INTERIM_CSV_BASE_FILEPATH'],
        csv_filename
    )
    return dataset_interim_folder_save_path


def build_interin_datasets():
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
        dataset_name = get_dataset_name_from_filename(full_path_filename)

        print("Applying base transformations to dataset",
              full_path_filename.split(os.sep)[-1])
        transformed_df = apply_common_transformations_to_dataset(
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
            all_dataframes[dataset_name] = add_wins_losses_by_season(
                all_dataframes[dataset_name], all_dataframes[advanced_df_key])
        print(f"---- ENDS PROCESSING {FILENAME} ----")

    print("SUCCESS")
    for dataset_name, dataframe in all_dataframes.items():
        filename = get_filename_from_dataset_name(dataset_name)
        FILENAME = filename.split(os.sep)[-1]
        print(f"---- SAVING FILE INTO {FILENAME} ----")
        print(f"STORING {dataset_name} in {filename}")
        dataframe.to_csv(filename, index=False)
        print("---- SUCCESS ----")


build_interin_datasets()
