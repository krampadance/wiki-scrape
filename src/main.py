import argparse
import logging

from src.tasks.scrape_hurricanes_to_csv import scrape_hurricanes_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s [%(asctime)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Scrape hurricane data from a Wikipedia URL and save to a CSV file."
    )
    parser.add_argument(
        "url",
        type=str,
        help="The Wikipedia URL of the hurricane season",
        default="https://en.wikipedia.org/wiki/1975_Pacific_hurricane_season",
        nargs="?",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="The name of the output CSV file",
        default="hurricanes.csv",
        nargs="?",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    try:
        scrape_hurricanes_to_csv(args.url, args.filename)
    except Exception as e:
        logger.error(e)
