import requests
import pandas as pd

from src.utils.constants import get_scraping_constants, get_folders_constants

scraping_constants = get_scraping_constants()
external_csv_base_folder = get_folders_constants()[
    'EXTERNAL_CSV_BASE_FILEPATH']


def scrape_stats_and_generate_csvs(
    last_year: int = scraping_constants['LAST_YEAR'],
    n_previous_years: int = scraping_constants['N_PREVIOUS_YEARS'],
    csv_base_filepath: str = external_csv_base_folder
) -> None:
    """_summary_

    Args:
        last_year (int, optional): _description_. Defaults to scraping_constants['LAST_YEAR'].
        n_previous_years (int, optional): _description_. Defaults to scraping_constants['N_PREVIOUS_YEARS'].
        csv_base_filepath (str, optional): _description_. Defaults to scraping_constants['CSV_BASE_FILEPATH'].
    """
    years_range = range(last_year - n_previous_years, last_year + 1)

    for current_year in years_range:
        print("------------------------------------------------------------")
        print(f"🕷️🕷️ Scraping data for {current_year}. 🕷️🕷️")
        response = requests.get(
            scraping_constants['SEASON_SUMMARY_URL'].format(current_year))
        if response.status_code == 404:
            continue
        print("Success! 🚀🚀")
        data = response.text
        for folder_name, dataset_table_id in scraping_constants['FOLDER_TO_ID_HASH'].items():
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
                f"{csv_base_filepath}/{folder_name}/{folder_name}_{current_year}.csv")
            print(f"💪💪 Success! 💪💪")
