import re

from src.utils.file_utils import save_file
from src.utils.llm_utils import query_llm
from src.utils.web_utils import fetch_webpage, scrape_webpage

hurricane_seasons = [
    "1975_Atlantic_hurricane_season",
    "1975_Pacific_hurricane_season",
    "1975_North_Indian_Ocean_cyclone_season",
]

if __name__ == "__main__":
    for hurricane_season in hurricane_seasons:
        print(hurricane_season)
        url = f"https://en.wikipedia.org/wiki/{hurricane_season}"
        webpage = fetch_webpage(url)
        scraped_data = scrape_webpage(webpage)

        prompt = f"""
            Given the following data, could you please extract the list of hurricanes(hurricane_storm_name), their start date(date_start), end date(date_end), number of deaths(number_of_deaths) and the 
            list of areas affected(list_of_areas_affected)?
            {scraped_data.model_dump()}
            Please provide results in csv format, as a string.
            Just the string, use comma as the delimitter and double quotes as separator.
            Replace "None" with "N/A" in column list_of_areas_affected
        """
        result = query_llm(prompt)

        csv_match = re.search(r"```csv\n(.*?)\n```", result, re.DOTALL)
        if csv_match:
            csv_data = csv_match.group(1)
        else:
            csv_data = result
        # Specify the file name
        filename = f"data/{hurricane_season}.csv"
        # Save File
        save_file(filename, csv_data)
