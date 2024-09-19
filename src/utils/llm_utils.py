import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.models.hurricane import HurricaneData
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


def query_llm_fc(page_data: PageData):
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
                            "name": {
                                "type": "string",
                                "description": "The name of the hurricane or storm.",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "The date the hurricane started.",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "The date the hurricane ended.",
                            },
                            "fatalities": {
                                "type": "integer",
                                "description": "The number of fatalities caused by the hurricane.",
                            },
                            "affected_areas": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "The areas affected by the hurricane.",
                            },
                        },
                        "required": ["name"],
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
        model="gpt-4",  # Use GPT model that supports function calling
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts hurricane information such as name, start and end date, fatalities and places affected by it, from text.",
            },
            {
                "role": "user",
                "content": f"Here is the page data: {page_data.model_dump_json()}",
            },
        ],
        functions=[function_schema],
        function_call={"name": "extract_hurricane_info"},
    )
    res = json.loads(response.choices[0].message.function_call.arguments)
    result = []
    for hurricane in res["hurricanes"]:
        result.append(HurricaneData(**hurricane))
    return result
