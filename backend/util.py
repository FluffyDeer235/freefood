from google import genai
from dotenv import load_dotenv
from schema import AnalysisResult
import os
import re


# Compiling keywords related to food that will be used to filter out posts that does not mention any food
FOOD_KEYWORDS = [
    "free", "food", "pizza", "bbq", "barbecue", "sizzle",
    "catered", "catering", "snacks", "drinks", "beverages",
    "refreshments", "lunch", "dinner", "breakfast", "supper",
    "boba", "coffee", "pastries", "donuts", "tacos"
]
FOOD_REGEX = re.compile(r"\b(" + "|".join(FOOD_KEYWORDS) + r")\b", re.IGNORECASE)


# Loading Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
INSTRUCTIONS = "You are an AI that analyzes university societies' event post captions. Determine if the post is advertising an event that has free food. Only flag it if food is explicitly mentioned as free or included"


def get_response(caption: str) -> dict:
    # Getting the response (whether event has free food) from gemini (To be changed to local model)
    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=caption,
        system_instruction=INSTRUCTIONS,
        generation_config={"temperature": 0.1},
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": AnalysisResult.model_json_schema()
        }
    )

    return AnalysisResult.model_validate_json(response.output_text).model_dump()

def update_database(response: dict, society: str) -> None:
    # add database integration
    print(response["price"])
    print(response["time"])
    print(response["location"])

def food_keyword_check(text: str) -> bool:
    # Check post information for keywords related to food
    return bool(FOOD_REGEX.search(text))