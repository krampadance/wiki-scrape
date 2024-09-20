# wiki-scrape
Wiki scrape intends to scrape a wikipedia page and structure the scraped date in a CSV file
In this initial stages of development it is designed to scrape hurricane data, based on the 
[1975 Pacific Hurricane Season page](https://en.wikipedia.org/wiki/1975_Pacific_hurricane_season)

# Methodology
## Data Collection
The data collection process leverages the requests library to retrieve the HTML content of web pages, specifically targeting Wikipedia.

## Scraping
The goal of the scraping process is to extract structured data from web pages that can be generalized across other types of documents, like books or articles. Wikipedia pages, for example, contain various sections and subsections, which are structured similarly to documents with headings, paragraphs, tables, and images.

To handle this variability, I introduced the PageData model, which captures essential metadata about the WikiPage and organizes its content into sections. This generalized structure allows the model to adapt to various data sources.

In the initial version (minimum viable product), the focus is on extracting textual content from Wikipedia. The `mw-content` div is targeted, which contains most of the textual information on Wikipedia pages. Sections and subsections are identified using the `mw-heading` classes (e.g., mw-heading1) or corresponding `<h>` tags (e.g., `<h1>, <h2>`). For simplicity, only `<p>` (paragraph) tags are collected in this version, leaving out tables, images, and captions.

The data between these sections is extracted, cleaned, and processed for storage in the PageData model. Special characters are sanitized, and references (e.g., [2], [3]) are removed to clean up the text.

## Query LLM
Once the data is scraped and structured in the PageData model, it is processed and fed to a large language model (LLM) using the OpenAI API. The goal is to extract insights or further structure the data in a meaningful way.

The OpenAI API supports function calling, which allows the LLM to return information in a structured, predictable manner. This helps ensure that the output is consistent and easy to parse programmatically.

The model’s parameters (e.g., temperature) are adjusted to produce deterministic answers. This reduces randomness, making the LLM’s output more stable and predictable. By setting the temperature to a low value (close to 0), the model provides responses that are more focused and reproducible, minimizing variability in the output.

## Storage
After receiving the structured data from the LLM, the results are saved to a CSV file for further analysis or storage. Storing the output in CSV format ensures easy readability, processing, and future use for reporting or data visualization.

# Improvements:
## Section Hierarchy:
Implement a tree-like structure for sections and subsections by adding id and parent_id attributes to the PageData model. This will allow sections to be nested appropriately, preserving the hierarchical nature of the content.
    
## Content Capture:
Collect more content than just the paragraph elements.
    - Tables: Collect `<table>` elements, parse them, and store the data in a structured format such as lists or dictionaries.
    - Images and Captions: Extract `<img>` tags and their associated captions. Store metadata like image URLs and caption or description.
    - Links: Capture `<a>` tags. Currently no information is captured in the References or See Also sections.
    
## Generalized Scraping:
The current model focuses on Wikipedia, but further generalization would involve abstracting the scraping process to handle other websites or document types (e.g., blogs, academic papers). This could be achieved by creating modular scrapers that adapt to different website structures.

## Split function calling 
We can split function calling in multiple functions to retrieve information separately, than altogether.

## Divide data in smaller chunks
LLM has token limits for each model. So in order not to reach this limit in a single query, we could divide the data in smaller parts and query the model sequentially.

## Define better prompts
I tried different prompts and the results differed from prompt to prompt. So the way one interacts with the model is of high importance.

# Code structure
In src folder the code is organized as:

- main.py: The main script to run and do the whole flow
- utils/ : Utility functions.
1. web_utils.py: Functions related with getting url data and scraping
2. text_utils.py: Functions related with text cleaning
3. llm_utils.py: Functions related with the llm, like querying
4. file_utils.py: Functions related with files, like saving csv file

- models/ : Classes representing data across the project. 

# TODO
- requirments.txt
- Dockerize
- Use command prompt input
- Exceptions
- Tests