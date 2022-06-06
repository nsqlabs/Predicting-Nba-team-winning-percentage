from src.data.etl import apply_transformation_to_datasets, extract_datasets_from_source


def run_etl():
    try:
        extract_datasets_from_source()
        apply_transformation_to_datasets()
    except Exception as error:
        print("Occured an error: ", error)