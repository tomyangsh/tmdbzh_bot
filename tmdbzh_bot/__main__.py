import re
import aiocron

from .client import client

from .handler import inline_handler, start_handler, inline_result_handler, imdb_handler

from . import rss

from pyrogram import filters

bot = client()

def imdb_filter(_, __, message):
    if message.text:
        if re.match('tt\d+', message.text):
            return True
    else:
        return False

imdb_filter = filters.create(imdb_filter)

@bot.on_inline_query()
async def inline_query(client, inline_query):
    await inline_handler(inline_query)

@bot.on_message(filters.command('start'))
async def start(client, message):
    await start_handler(message, bot)

@bot.on_chosen_inline_result()
async def edit_inline_result(client, result):
    await inline_result_handler(result, bot)

@bot.on_message(imdb_filter)
async def public(client, message):
    await imdb_handler(message)

@aiocron.crontab('*/30 * * * *')
async def push_rss():
    item_list = rss.fetch()
    for item in item_list:
        await bot.send_message(-1001195256281, item, disable_web_page_preview=True)

bot.run()
