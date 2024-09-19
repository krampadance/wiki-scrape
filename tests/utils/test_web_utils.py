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

    assert result.sections[0].title == "1975 Pacific hurricane season"

    assert result.sections[0].id == "firstHeading"
    assert (
        result.sections[0].text
        == "The 1975 Pacific hurricane season officially started May 15, 1975, in the eastern Pacific, and June 1, 1975, in the central Pacific, and lasted until November 30, 1975. These dates conventionally delimit the period of each year when most tropical cyclones form in the northeast Pacific Ocean.The 1975 Pacific hurricane season was slightly above average, with 17 tropical storms forming. Of these, 9 became hurricanes, and 4 became major hurricanes by reaching Category 3 or higher on the Saffir-Simpson Hurricane Scale. The only notable storms are Hurricane Olivia, which killed 30 people, caused 30 million (1975 USD) in damage, and left thousands homeless when it made landfall in October; and an unnamed hurricane that developed at very high latitude, but had no effect on land. Hurricane Denise was the strongest storm of the year. Hurricanes Lily and Katrina passed close to Socorro Island and Tropical Storm Eleanor made landfall in Mexico. Hurricane Agatha sank a ship."
    )
    assert result.sections[1].title == "Season summary"

    assert result.sections[1].id == "Season_summary"

    assert result.sections[2].title == "Systems"
    assert result.sections[2].text == ""
    assert result.sections[2].id == "Systems"

    expected_sections = [
        "1975 Pacific hurricane season",
        "Season summary",
        "Systems",
        "Hurricane Agatha",
        "Tropical Storm Bridget",
        "Hurricane Carlotta",
        "Hurricane Denise",
        "Tropical Storm Eleanor",
        "Tropical Storm Francene",
        "Tropical Storm Georgette",
        "Tropical Storm Hilary",
        "Hurricane Ilsa",
        "Hurricane Jewel",
        "Hurricane Katrina",
        "Unnamed hurricane",
        "Hurricane Lily",
        "Tropical Storm Monica",
        "Tropical Storm Nanette",
        "Hurricane Olivia",
        "Tropical Storm Priscilla",
        "Other systems",
        "Storm names",
        "See also",
        "References",
        "External links",
    ]
    collected_sections = list()
    for section in result.sections:
        collected_sections.append(section.title)
    # Assert it collects expected sections
    assert len(set(expected_sections) - set(collected_sections)) == 0
    print(result.model_dump())
