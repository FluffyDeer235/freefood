import instaloader
import itertools
import random
import time
import util


L = instaloader.Instaloader()
NUM_POSTS = 3

#Find a way to get society/club name
societies = ["uts_cps"]

for username in societies:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()

    for post in itertools.islice(posts, NUM_POSTS):
        if not post.caption:
            continue
        caption = post.caption + f" (posted at {post.date_local})"

        #Feed caption to AI, output should be a dict with stuff
        response = util.get_response(caption)

        if response["is_event"] and response["has_food"]:
            util.update_database(response, username)


    time.sleep(random.randint(25, 37))
    