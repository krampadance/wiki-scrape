import csv
import os

from dotenv import load_dotenv

from src.models.hurricane_data import HurricaneData

load_dotenv()

DATA_FOLDER = os.getenv("DATA_FOLDER") or "data"


def save_file(filename: str, data: str) -> None:
    """Saves string data to a file

    Args:
        filename (str): The filename of the file
        data (str): The data to be stored in the file as a string
    """
    # Write the CSV data to a file
    with open(filename, "w", newline="") as file:
        file.write(data.strip())


def save_hurricane_file(filename: str, data: list[HurricaneData]) -> None:
    """Functions that save hurricane data specifically to a csv file.
    The lines of the csv file are from the list of the data passed

    Args:
        filename (str): The filename
        data (list[HurricaneData]): Hurricane data, each object contains
         data for one hurricane
    """
    hurricane_dicts = [h.model_dump(by_alias=True) for h in data]

    # Convert 'places' (a list) into a string for CSV
    for hurricane in hurricane_dicts:
        hurricane["list_of_areas_affected"] = ", ".join(
            hurricane["list_of_areas_affected"]
        )

    csv_headers = hurricane_dicts[0].keys()

    # Write the data to a CSV file
    with open(f"{DATA_FOLDER}/{filename}", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)

        # Write the header (using aliases as columns)
        writer.writeheader()

        # Write each row of hurricane data
        writer.writerows(hurricane_dicts)
