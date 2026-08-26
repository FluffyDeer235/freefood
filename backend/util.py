from google import genai
from dotenv import load_dotenv
from schema import AnalysisResult
import os

# Loading Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
INSTRUCTIONS = "You are an AI that analyzes university societies' Instagram post captions. Determine if the post is advertising an event that has free food. Only flag it if food is explicitly mentioned as free or included"

def get_response(caption: str) -> dict:
    # Getting the response (whether event has free food) from gemini (To be changed to local model)
    response = client.interactions.create(
        model="gemini-2.5-flash",
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
    pass