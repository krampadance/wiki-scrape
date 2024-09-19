import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.models.hurricane_data import HurricaneData
from src.models.page_data import PageData

# Load environment variables from the .env file
load_dotenv()


def query_llm(prompt: str):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content


def query_hurricane_data(page_data: PageData):
    function_schema = {
        "name": "extract_hurricane_info",
        "description": "Extracts hurricane information from the text, such as name, start and end date and fatalities.",
        "parameters": {
            "type": "object",
            "properties": {
                "hurricanes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "hurricane_storm_name": {
                                "type": "string",
                                "description": "The name of the hurricane or storm.",
                                "nullable": True,
                            },
                            "date_start": {
                                "type": "string",
                                "description": "The date the hurricane started.",
                                "nullable": True,
                            },
                            "date_end": {
                                "type": "string",
                                "description": "The date the hurricane ended.",
                                "nullable": True,
                            },
                            "number_of_deaths": {
                                "type": "integer",
                                "description": "The number of deaths caused by the hurricane.",
                                "nullable": True,
                            },
                            "list_of_areas_affected": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "The areas affected by the hurricane.",
                                "nullable": True,
                            },
                        },
                        "required": ["hurricane_storm_name"],
                    },
                }
            },
        },
    }
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o",  # Use GPT model that supports function calling
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts hurricane and storm information such as name, start and end date, deaths and places affected by it, from text.",
            },
            {
                "role": "user",
                "content": f"Here is the page data organized in sections from the web page and their textual content: {page_data.model_dump_json()}. We want all the hurricanes and storms listed in the texts.",
            },
        ],
        functions=[function_schema],
        function_call={"name": "extract_hurricane_info"},
        temperature=0.2,  # Set to 0 for consistent results
        max_tokens=1000,  # Limit the output length if needed
        n=1,  # Number of completions to generate
        stop=None,
    )
    res = json.loads(response.choices[0].message.function_call.arguments)
    result = []
    for hurricane in res["hurricanes"]:
        result.append(HurricaneData(**hurricane))
    return result
