from bs4 import BeautifulSoup
import requests
import time
from util import *

HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 OPR/135.0.0.0 (Edition std-2)",
    "Referer": "https://www.activateuts.com.au/events/?orderby=upcoming&event_date=7",
    "Accept": "application/json"
}

SEEN_EVENTS: set[int] = get_seen_events()

def scrap():

    prune_events()

    request = requests.get(activate_api(1), headers=HEADERS)

    if request.status_code == 200:
        num_pages: int = int(request.headers.get("X-Wp-Totalpages"))
        scan_page(request.json())

        for i in range(2, num_pages + 1):
            print(f"page{i}")
            request = requests.get(activate_api(i), headers=HEADERS)

            if request.status_code == 200:
               scan_page(request.json())

def scan_page(events: list[dict]):
    for event in events:
        event_id: int = event["id"]
        print(event_id)

        # If event has already been seen before, skip through it
        if event_id in SEEN_EVENTS:
            print("skipped")
            continue

        end_date, end_time = event["acf"]["end_date"].split(maxsplit=1)
        start_date, start_time = event["acf"]["start_date"].split(maxsplit=1)
        event_link: str = event["link"]
        post_title: str = event["title"]
        post_desc1: str = event["acf"]["hero"]["description"]
        post_desc2: str = BeautifulSoup(event["acf"]["html"], "html.parser").get_text()
        post_faqs: list | bool = event["acf"]["faqs"]["sections"] # If the post doesn't have faqs, the field is False

        # Cleaning up faqs into a string to run checks
        if not post_faqs:
            faqs = ""
        else:
            faqs = []

            for q in post_faqs:
                faqs.append(f"{q["title"]}: {BeautifulSoup(q["content"], "html.parser").get_text()}")

            faqs = ". ".join(faqs)

        # Combining all event info into a string
        info_string: str = " ".join([post_title, post_desc1, post_desc2, faqs])

        # If the string contained no mention of food, skip to the next event
        if not food_keyword_check(info_string):
            update_database(
                event_id, 
                False,
                post_title,
                event_link,
                False, 
                get_datetime(end_date, end_time),
                get_datetime(start_date, start_time)
            )
            continue

        results = get_response(info_string)
        update_database(
            event_id,
            results["has_food"], 
            post_title, 
            event_link, 
            results["is_free"],
            get_datetime(end_date, end_time),
            get_datetime(start_date, start_time)
        )

    time.sleep(2)

       
if __name__ == "__main__":
    scrap()
    