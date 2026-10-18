import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from backend.util import get_food_events
from datetime import datetime

load_dotenv()
token = os.getenv("BOT_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Ready.")

@bot.command()
async def free_food(ctx):
    events = get_food_events()

    if not events:
        await ctx.send("No free food events found right now! 😢")
        return

    current_message = "**🍔 Upcoming Events with food 🍕**\n \n"
    messages = []

    for event in events:
        title: str = event["title"]
        link: str = event["link"]
        start_datetime: datetime = event["start_datetime"]
        end_datetime: datetime = event["end_datetime"]
        is_free: bool = event["is_free"]

        start_str = start_datetime.strftime("%b %d, %I:%M %p")
        end_str = end_datetime.strftime("%b %d, %I:%M %p")
        time_display = f"{start_str} - {end_str}"

        event_str: str = f"**[{title}]({link})**\n 🎟️ {"Free/Included in Ticket" if is_free else "Not Free"}\n 📆 {time_display} \n \n"

        if len(current_message) + len(event_str) > 1950:
            messages.append(current_message)
            current_message = event_str
        else:
            current_message += event_str

    if current_message:
        messages.append(current_message)
    
    for message in messages:
        await ctx.send(message)
            

bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
