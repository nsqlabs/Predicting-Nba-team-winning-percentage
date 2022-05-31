import os
from .constants import get_folders_constants, get_scraping_constants


def generate_full_csv_filename(file_type: str, data_state: str) -> str:
    to_year = get_scraping_constants()['LAST_YEAR']
    from_year = to_year - get_scraping_constants()['N_PREVIOUS_YEARS']

    return os.path.join(
        get_folders_constants()['CSV_BASE_FILEPATH'],
        data_state,
        f"{file_type}_{data_state}_{from_year}_{to_year}.csv", )
