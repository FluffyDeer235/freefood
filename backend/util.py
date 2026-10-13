from google import genai
from dotenv import load_dotenv
from schema import AnalysisResult
import os
import re
import psycopg
from datetime import datetime
from zoneinfo import ZoneInfo
from tenacity import retry, wait_exponential, stop_after_attempt


# Compiling keywords related to food that will be used to filter out posts that does not mention any food
FOOD_KEYWORDS = [
    "free", "food", "pizza", "bbq", "barbecue", "sizzle",
    "catered", "catering", "snacks", "drinks", "beverages",
    "refreshments", "lunch", "dinner", "breakfast", "supper",
    "boba", "coffee", "pastries", "donuts", "tacos", "dishes",
    "sushi", 
]
FOOD_REGEX = re.compile(r"\b(" + "|".join(FOOD_KEYWORDS) + r")\b", re.IGNORECASE)


# Loading Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
INSTRUCTIONS = "You are an AI that analyzes university societies' event post captions. Determine if the post is advertising an event that has free food. Only flag it if food is explicitly mentioned as free or included"

# 
CONNECTION_URL = os.getenv("CONNECTION_URL")

@retry(wait=wait_exponential(multiplier=2, min=2, max=20), stop=stop_after_attempt(5))
def get_response(caption: str) -> dict:
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

def get_seen_events() -> set[int]:
    try:
        with psycopg.connect(CONNECTION_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM events;")

                return {row[0] for row in cur.fetchall()}
    except Exception as e:
        print(f"Error in getting seen events: {str(e)}")
        return set()

def prune_events() -> None:
    try:
        with psycopg.connect(CONNECTION_URL) as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM events WHERE end_datetime < %s;"
                cur.execute(query, (datetime.now(ZoneInfo("Australia/Sydney")), ))

            conn.commit()
    except Exception as e:
        print(f"Error pruning events: {str(e)}")

def update_database(event_id: int, has_food: bool, title=None, link=None, is_free=None, end_datetime=None, start_datetime=None) -> None:
    try:
        with psycopg.connect(CONNECTION_URL) as conn:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO events ("id", "title", "link", "has_food", "is_free", "end_datetime", "start_datetime")
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """

                values = (event_id, title, link, has_food, is_free, end_datetime, start_datetime)

                cur.execute(query, values)
            conn.commit()
    except Exception as e:
        print(f"Error in updating database: {str(e)}")

def get_food_events() -> list[dict]:
    try:
        with psycopg.connect(CONNECTION_URL) as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT title, link, start_datetime, end_datetime 
                    FROM events 
                    WHERE has_food = TRUE 
                    AND end_datetime >= %s
                    ORDER BY start_datetime ASC;
                """

                cur.execute(query, (datetime.now(ZoneInfo("Australia/Sydney")), ))

                return [{
                    "title": row[0],
                    "link": row[1],
                    "start_datetime": row[2],
                    "end_datetime": row[3]
                } for row in cur.fetchall()]
    except Exception as e:
        print(f"Error in getting events with food: {str(e)}")
        return []

# Check post information for keywords related to food
def food_keyword_check(text: str) -> bool:
    return bool(FOOD_REGEX.search(text))

# Returns the api link the scrapper will hit based on the current page
def activate_api(page_num: int) -> str:
    return f"https://www.activateuts.com.au/wp-json/wp/v2/events?per_page=15&page={page_num}&event_date=7&orderby=upcoming"

# Converts the end date and end time to a datetime object 
def get_datetime(date: str, time:str) -> datetime:
    return datetime.strptime(f"{date} {time}", "%d/%m/%Y %I:%M %p").replace(tzinfo=ZoneInfo("Australia/Sydney"))
