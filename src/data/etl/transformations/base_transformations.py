import numpy as np
import pandas as pd
from src.utils.constants import get_scraping_constants

def _add_season_to_dataframe(team_series):
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


def add_wins_losses_by_season(stats_df, advanced_stats_df):
    print(stats_df.columns)

    stats_df_copy = stats_df.copy()  # copy input df
    stats_df_copy.loc[:, ['W', 'L']] = advanced_stats_df.loc[:, [
        'W', 'L']].copy()  # extract wins and losses column
    stats_df_copy = stats_df_copy.sort_values(
        by=["Season", "W", "Playoffs"],
        ascending=[False, False, True]
    ).reset_index(drop=True)
    return stats_df_copy


def apply_common_transformations_to_dataset(stats_df: pd.DataFrame) -> pd.DataFrame:
    final_df = stats_df.copy()

    # Adding season prop to the dataset
    final_df['Season'] = _add_season_to_dataframe(final_df.Team)

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
