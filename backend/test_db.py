import psycopg
from util import *
from datetime import datetime

def main():
    events_with_food = get_food_events()

    for e in events_with_food:
        print(f"{e["title"]}: {e["link"]}.  Starts at: {e["start_datetime"]}, ends at: {e["end_datetime"]}")


if __name__ == "__main__":
    main()
