<<<<<<< HEAD
import instaloader
import random
import time
import itertools
import util
=======
from apscheduler import BlockingScheduler
from scrapper import scrap
>>>>>>> 44da84b48ce551d6b3eb36135e35d49419d267ca

def main():
    scheduler: BlockingScheduler = BlockingScheduler()
    scheduler.add_job(scrap, "cron", day = "*", hour = "1")

    scheduler.start()

<<<<<<< HEAD
#Find a way to get society/club name
societies = []

for username in societies:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()

    for post in itertools.islice(posts, NUM_POSTS):
        caption = posts.caption

        #Feed caption to AI, output should be a dict with stuff
        response = util.get_response(caption)

        if response["is_event"]:
            util.update_database(response)

    time.sleep(random.randint(25, 37))
    
=======
if __name__ == "__main__":
    main()
>>>>>>> 44da84b48ce551d6b3eb36135e35d49419d267ca
