import os

from dotenv import load_dotenv
from openai import OpenAI

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
