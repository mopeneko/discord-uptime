from datetime import datetime
import os
import time
import threading
from typing import Dict

from discord.ext import commands
import requests

statuses: Dict[str, bool] = {}
check_time = datetime.now()


def check():
    while True:
        for url in statuses:
            try:
                requests.get(url, timeout=5)
                statuses[url] = True
            except:
                statuses[url] = False

        check_time = datetime.now()
        time.sleep(60)


thread = threading.Thread(target=check)
thread.start()

bot = commands.Bot(command_prefix="-")


@bot.command()
async def check(ctx):
    result = ""

    for url, status in statuses.items():
        result += f"{url}: {status}\n"

    result += f"check time: {check_time.strftime('%Y-%m-%d %H:%M:%S')}"

    await ctx.send(result)


@bot.command()
async def add(ctx, url):
    if url in statuses:
        return await ctx.send("URL is already registered")
    statuses[url] = False
    await ctx.send("Added!\nThe status is become False until checking will start")


@bot.command()
async def remove(ctx, url):
    if url not in statuses:
        return await ctx.send("URL is not registered")
    del statuses[url]
    await ctx.send("Removed!")


bot.run(os.getenv("DISCORD_TOKEN"))
