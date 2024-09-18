import requests
from bs4 import BeautifulSoup

from src.models.page_data import PageData, PageMetadata, SectionData
from src.utils.text_utils import clean_text


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


def collect_elements(child, element, heading_tag, ending_class, parent_id):
    section_content = []
    next_sibling = child.find_next_sibling()
    # Collect content until the next heading or a non-paragraph element
    while next_sibling and ending_class not in next_sibling.get("class", []):
        if next_sibling.name == element:
            section_content.append(clean_text(next_sibling.get_text().strip()))
        next_sibling = next_sibling.find_next_sibling()

    # Create and return the section data
    return SectionData(
        title=clean_text(child.find(heading_tag).text.strip()) or "No title",
        parent_id=parent_id,
        text=" ".join(section_content),
        id=child.find(heading_tag).get("id") or "No id",
        element_type=element,
    )


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
    sections: list[SectionData] = []
    parent_id = None
    heading = soup.find(id="firstHeading")

    headsection = SectionData(
        title=clean_text(heading.text.strip()),
        parent_id=parent_id,
        id="firstHeading",
        element_type="h1",
    )

    body_content = soup.find(id="mw-content-text")
    # test = collect_elements(body_content, "p", None, "mw-heading", "mw-content-text")
    parent_id = "firstHeading"
    for child in body_content.find_all("div"):
        class_list = child.get("class")

        if class_list and "mw-content-ltr" in class_list:
            section = collect_elements(child, "p", None, "mw-heading", parent_id)
        if class_list and "mw-heading" in class_list:
            # For mw-heading2 sections
            if "mw-heading2" in class_list:
                section = collect_elements(child, "p", "h2", "mw-heading", parent_id)
                sections.append(section)
                parent_id = section.id  # Update parent_id for nested sections

            # For mw-heading3 sections
            elif "mw-heading3" in class_list:
                section = collect_elements(child, "p", "h3", "mw-heading", parent_id)
                sections.append(section)
    return PageData(
        title=soup.head.title.text,
        sections=sections,
        metadata=PageMetadata(
            url="test",
            last_updated=soup.find(id="footer-info-lastmod").text,
        ),
    )
