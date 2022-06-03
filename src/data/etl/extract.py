import requests
import pandas as pd
import os

from src.utils.constants import get_scraping_constants, get_folders_constants
from src.data.etl._utils import generate_full_csv_filename

SCRAPING_CONSTANTS = get_scraping_constants()
EXTERNAL_CSV_BASE_FOLDER = get_folders_constants()[
    'EXTERNAL_CSV_BASE_FILEPATH']


def _scrape_stats_and_generate_csvs(
    last_year: int = SCRAPING_CONSTANTS['LAST_YEAR'],
    n_previous_years: int = SCRAPING_CONSTANTS['N_PREVIOUS_YEARS'],
    csv_base_filepath: str = EXTERNAL_CSV_BASE_FOLDER
) -> None:
    """_summary_

    Args:
        last_year (int, optional): _description_. Defaults to SCRAPING_CONSTANTS['LAST_YEAR'].
        n_previous_years (int, optional): _description_. Defaults to SCRAPING_CONSTANTS['N_PREVIOUS_YEARS'].
        csv_base_filepath (str, optional): _description_. Defaults to SCRAPING_CONSTANTS['CSV_BASE_FILEPATH'].
    """
    years_range = range(last_year - n_previous_years, last_year + 1)

    for current_year in years_range:
        print("------------------------------------------------------------")
        print(f"🕷️🕷️ Scraping data for {current_year}. 🕷️🕷️")
        response = requests.get(
            SCRAPING_CONSTANTS['SEASON_SUMMARY_URL'].format(current_year))
        if response.status_code == 404:
            continue
        print("Success! 🚀🚀")
        data = response.text
        for folder_name, dataset_table_id in SCRAPING_CONSTANTS['FOLDER_TO_ID_HASH'].items():
            print(f"👀👀 Reading html files for {current_year}. 👀👀")
            if folder_name != 'advanced_stats':
                dataframe = pd.read_html(
                    data, attrs={'id': dataset_table_id},  header=0)[0]
            else:
                dataframe = pd.read_html(
                    data, attrs={'id': dataset_table_id},  header=1)[0]
            print(
                f"💾💾 Saving csv file for {current_year}'s {folder_name} data. 💾💾")
            dataframe.to_csv(
                f"{csv_base_filepath}/{folder_name}/{folder_name}_{current_year}.csv",
                index=False
            )
            print(f"💪💪 Success! 💪💪")


def _create_totals_raw_datasets() -> None:
    EXTERNAL_CSV_BASE_FILEPATH = get_folders_constants()[
        'EXTERNAL_CSV_BASE_FILEPATH']

    scraped_data_csv_folders_csv_folders = list(filter(
        lambda filename: filename.endswith('stats'), os.listdir(EXTERNAL_CSV_BASE_FILEPATH))
    )

    for folder in scraped_data_csv_folders_csv_folders:
        print("------------------------------------------------------------")
        print(f"Creating full dataset for {folder} folder")

        folder_csv_files_path = os.path.join(
            EXTERNAL_CSV_BASE_FILEPATH, folder)

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

def extract_datasets_from_source():
    _scrape_stats_and_generate_csvs()
    _create_totals_raw_datasets()
    
extract_datasets_from_source()