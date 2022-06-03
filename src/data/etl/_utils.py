import os
from src.utils.constants import get_folders_constants, get_scraping_constants


def get_raw_dataset_name_from_filename(filename):
    return f"{filename.split(os.sep)[-1].split('_raw_')[0]}_interim_df"


def create_interim_filename_from_dataset_name(dataset_name):
    # remove _df and append .csv
    csv_filename = f"{dataset_name.split('_df')[0]}.csv"
    print(csv_filename)
    dataset_interim_folder_save_path = os.path.join(
        get_folders_constants()['INTERIM_CSV_BASE_FILEPATH'],
        csv_filename
    )
    return dataset_interim_folder_save_path

def generate_full_csv_filename(file_type: str, data_state: str) -> str:
    to_year = get_scraping_constants()['LAST_YEAR']
    from_year = to_year - get_scraping_constants()['N_PREVIOUS_YEARS']

    return os.path.join(
        get_folders_constants()['CSV_BASE_FILEPATH'],
        data_state,
        f"{file_type}_{data_state}_{from_year}_{to_year}.csv", )