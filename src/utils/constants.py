import os
from typing import Union, Dict, List
from .folders import get_root_folder


CONSTANTS: Dict[str, Union[int, str, Dict, List]] = {
    'FOLDERS': {
        'CSV_BASE_FILEPATH': os.path.join(get_root_folder(), "data"),
        'EXTERNAL_CSV_BASE_FILEPATH': os.path.join(get_root_folder(), "data", "external"),
        'INTERIM_CSV_BASE_FILEPATH': os.path.join(get_root_folder(), "data", "interim"),
        'PROCESSED_CSV_BASE_FILEPATH': os.path.join(get_root_folder(), "data", "processed"),
        'RAW_CSV_BASE_FILEPATH': os.path.join(get_root_folder(), "data", "raw"),

    },
    'SCRAPING': {
        'LAST_YEAR': 2022,
        'N_PREVIOUS_YEARS': 32,
        'SEASON_SUMMARY_URL': "https://www.basketball-reference.com/leagues/NBA_{}.html",
        'FOLDER_TO_ID_HASH':  {
            'per_game_stats': 'per_game-team',
            'per_100_possesions_stats': 'per_poss-team',
            'season_total_stats': 'totals-team',
            'advanced_stats': 'advanced-team'
        },
    }
}


def get_scraping_constants():
    return CONSTANTS['SCRAPING']


def get_folders_constants():
    return CONSTANTS['FOLDERS']
