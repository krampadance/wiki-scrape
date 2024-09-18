from src.utils.web_utils import fetch_webpage, scrape_webpage

url = "https://en.wikipedia.org/wiki/1975_Atlantic_hurricane_season"

if __name__ == "__main__":
    webpage = fetch_webpage(url)
    scraped_data = scrape_webpage(webpage)
    breakpoint()
