from bs4 import BeautifulSoup
import requests
from util import *

ACTIVATE_API: str = "https://www.activateuts.com.au/wp-json/wp/v2/events?per_page=15&page=1&event_date=7&orderby=upcoming"

HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 OPR/135.0.0.0 (Edition std-2)",
    "Referer": "https://www.activateuts.com.au/events/?orderby=upcoming&event_date=7",
    "Accept": "application/json"
}

def scrap():
    # Get seen_events from database

    request = requests.get(ACTIVATE_API, headers=HEADERS)

    if request.status_code == 200:
        num_pages: int = request.headers.get("X-Wp-Totalpages")
        events: list[dict] = request.json()

        for event in events:
            event_id: int = event["id"]

            # If event has already been seen before, skip through it
            # if event_id in seen_events:
            #   continue

            # Add event to seen events table

            event_link: str = event["link"]
            post_title: str = event["title"]
            post_desc1: str = event["acf"]["hero"]["description"]
            post_desc2: str = BeautifulSoup(event["acf"]["html"], "html.parser").get_text()
            post_faqs: list | bool = event["acf"]["faqs"]["sections"] # If the post doesn't have faqs, the field is False
            # event_location

            if not post_faqs:
                faqs = ""
            else:
                faqs = []

                for q in post_faqs:
                    faqs.append(f"{q["title"]}: {BeautifulSoup(q["content"], "html.parser").get_text()}")

                faqs = ". ".join(faqs)

            info_string: str = " ".join([post_title, post_desc1, post_desc2, faqs])

            if not food_keyword_check(info_string):
                print("event doesnt have food")
                continue

            print("event has food????")

            results = get_response(info_string)
            print("gemini asked")
            print(f"has food: {results["has_food"]}")
            print(f"is_free: {results["is_free"]}")

            # update to database
            return
        

if __name__ == "__main__":
    scrap()
    