import instaloader
import random
import time
import util


L = instaloader.Instaloader()
NUM_POSTS = 3

#Find a way to get society/club name
societies = []

for username in societies:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()

    for i in range(NUM_POSTS):
        caption = posts[i].caption

        #Feed caption to AI, output should be a dict with stuff
        response = util.get_response(caption)

        if response["is_event"]:
            util.update_database(response)


    time.sleep(random.randint(25, 37))
    