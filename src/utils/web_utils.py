import requests
from bs4 import BeautifulSoup

from src.models.page_data import PageData


# Function to fetch webpage content
def fetch_webpage(url: str, **kwargs) -> str:
    """Fetches the webpage requested by the url

    Args:
        url (str): The url of the webpage

    Returns:
        str: The string representation of the webpage
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad status
    return response.text


def scrape_webpage(content: str, **kwargs) -> PageData:
    """Scrapes the webpage

    Args:
        content (str): The content of the webpage

    Returns:
        PageData: An object structured representation of the web page's data
    """
    soup = BeautifulSoup(content, "html.parser")
    if soup.head is None:
        raise BaseException("Content is empty")
    return PageData(title=soup.head.title.text)
