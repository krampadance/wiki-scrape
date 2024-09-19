import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from src.models.page_data import PageData, PageMetadata, SectionData
from src.utils.text_utils import clean_text

# TODO: Collect references data
# TODO: Collect tables data
# TODO: Implement correct linking between sections.


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
    """Collects the elements specified in the next siblings of the child.
    If ending class is found we return the collected data

    Args:
        child (_type_): _description_
        element (_type_): _description_
        heading_tag (_type_): _description_
        ending_class (_type_): _description_
        parent_id (_type_): _description_

    Returns:
        _type_: _description_
    """
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


def collect_intro_section(
    body_content: Tag | NavigableString | None, first_heading: Tag | NavigableString
) -> list[str]:
    """Collects the intro section of the wiki page

    Args:
        body_content (Tag | NavigableString | None): The content of the body content of the wiki page
        first_heading (Tag | NavigableString): The Tag of the first heading that shows up, to be used as terminating condition

    Returns:
        list[str]: List of the text in <p> elements
    """
    section_content = []
    for sibling in body_content.find_all_next():
        if sibling == first_heading:
            break
        if sibling.name == "p":
            section_content.append(clean_text(sibling.get_text().strip()))
    return section_content


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

    # Get the body content
    body_content = soup.find(id="mw-content-text")
    # Get the list of headings of the page
    headings = body_content.find_all(class_="mw-heading")
    first_heading = headings[0]

    # Collect main section data
    intro_content = collect_intro_section(body_content, first_heading)

    heading = soup.find(id="firstHeading")
    sections.append(
        SectionData(
            title=clean_text(heading.text.strip()),
            parent_id=parent_id,
            id="firstHeading",
            element_type="h1",
            text="".join(intro_content),
        )
    )

    # Collect subsections data
    for child in headings:
        heading_class = child.get("class").pop()
        section = collect_elements(
            child, "p", f"h{heading_class[-1]}", "mw-heading", parent_id
        )
        sections.append(section)
    return PageData(
        title=soup.head.title.text,
        sections=sections,
        metadata=PageMetadata(
            url="test",
            last_updated=soup.find(id="footer-info-lastmod").text,
        ),
    )
