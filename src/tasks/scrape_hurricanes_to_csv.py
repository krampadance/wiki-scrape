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


# TODO: Make it more general, to pass prompts and function shemas
def scrape_hurricanes_to_csv(url: str, filename: str = "hurricanes.csv") -> None:
    """Scrapes the webpage provided and extracts hurricane data

    Args:
        url (str): The url of the page
        filename (str, optional): The filename to save the file. Defaults to "hurricanes.csv".
    """
    logger.info(f"Going to scrape {url}")
    webpage = fetch_webpage(url)
    logger.info("Fetched page successfully")
    scraped_data = scrape_webpage(webpage)
    logger.info("Scraped page successfully")
    logger.info("Contacting llm to retrieve hurricane info")
    result: list[HurricaneData] = query_hurricane_data(scraped_data)
    logger.info(f"Saving to {filename}")
    save_hurricane_file(filename, result)
