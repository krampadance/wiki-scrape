import logging

from src.models.hurricane_data import HurricaneData
from src.utils.file_utils import save_hurricane_file
from src.utils.llm_utils import query_hurricane_data
from src.utils.web_utils import fetch_webpage, scrape_webpage

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s [%(asctime)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

hurricane_seasons = [
    "1975_Atlantic_hurricane_season",
    "1975_Pacific_hurricane_season",
    "1975_North_Indian_Ocean_cyclone_season",
]


if __name__ == "__main__":
    url = f"https://en.wikipedia.org/wiki/{hurricane_seasons[1]}"
    logger.info(f"Going to scrape {url}")
    filename = f"{hurricane_seasons[1]}.csv"
    webpage = fetch_webpage(url)
    logger.info("Fetched page successfully")
    scraped_data = scrape_webpage(webpage)
    logger.info("Scraped page successfully")
    logger.info("Contacting llm to retrieve hurricane info")
    result: list[HurricaneData] = query_hurricane_data(scraped_data)
    logger.info(f"Saving to {filename}")
    save_hurricane_file(filename, result)
