from datetime import datetime

import pytest

from src.utils.web_utils import scrape_webpage


def test_scrape_webpage_empty_content() -> None:
    with pytest.raises(BaseException) as excinfo:
        scrape_webpage("")
    assert "Content is empty" == str(excinfo.value)


def test_scrape_hurricanes_content() -> None:
    content: str = None
    with open("tests/hurricanes-wiki.html", "r") as file:
        # Read the contents of the file
        content = file.read()
    result = scrape_webpage(content)
    assert result.title == "1975 Pacific hurricane season - Wikipedia"
    assert result.metadata.url == "test"
    assert result.metadata.last_updated == datetime(2024, 7, 20, 18, 53)
