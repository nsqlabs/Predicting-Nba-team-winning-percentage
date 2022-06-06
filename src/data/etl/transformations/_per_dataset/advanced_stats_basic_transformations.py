import pandas as pd


def _remove_unnecesary_columns(advanced_stats_full_dataset_preprocessed_df):
    SEPARATORS_COLUMNS = [
        column for column in advanced_stats_full_dataset_preprocessed_df.columns
        if column.startswith('Unnamed:')
    ]

    UNNECESARY_COLUMNS = [['Attend.', 'Attend./G', 'Arena']]

    return advanced_stats_full_dataset_preprocessed_df.drop(
        [*SEPARATORS_COLUMNS, *UNNECESARY_COLUMNS],
        axis=1
    )


def _rename_four_factor_columns(advanced_stats_full_dataset_preprocessed_df):
    def classify_feature_as_off_or_def(feature):
        if not feature.endswith('.1'):
            return f"offensive_{feature}"
        return f"defensive_{feature.replace('.1', '')}"

    COLUMNS_TO_RENAME = [
        'eFG%', 'TOV%', 'FT/FGA',
        'eFG%.1', 'TOV%.1', 'FT/FGA.1'
    ]

    return advanced_stats_full_dataset_preprocessed_df.rename(
        columns={
            old_key: classify_feature_as_off_or_def(old_key)
            for old_key in COLUMNS_TO_RENAME
        }
    )


def transform_advanced_stats_df(advanced_stats_full_dataset_interim_df):
    advanced_stats_full_dataset_preprocessed_df = advanced_stats_full_dataset_interim_df.copy()

    # Removing the unnecesary columns (incomplete, irrelevant and separators).
    advanced_stats_full_dataset_preprocessed_df = _remove_unnecesary_columns(
        advanced_stats_full_dataset_preprocessed_df)

    # Renaming similar columns due to 4 factors (offensive and defensive)
    advanced_stats_full_dataset_preprocessed_df = _rename_four_factor_columns(advanced_stats_full_dataset_preprocessed_df)
    
    return advanced_stats_full_dataset_preprocessed_df
