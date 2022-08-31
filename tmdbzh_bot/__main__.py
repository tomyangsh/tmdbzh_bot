import re
import aiocron

from . import bot
from .util import Inline_search_markup
from .handler import inline_handler, inline_result_handler, imdb_handler, callback_handler

from . import rss

from pyrogram import filters, enums

async def imdb_filter(_, __, message):
    if message.text:
        return re.match('tt\d+', message.text)

imdb_filter = filters.create(imdb_filter)

async def group_filter(_, __, message):
    me = await bot.get_me()
    return message.chat.type == enums.ChatType.PRIVATE or re.search(me.username, message.text)

group_filter = filters.create(group_filter)

@bot.on_inline_query()
async def inline_query(client, inline_query):
    await inline_handler(inline_query)

@bot.on_message(filters.command('start') & group_filter)
async def start(client, message):
    await message.reply_text("TMDb 影视及人物信息检索", reply_markup=Inline_search_markup)

@bot.on_chosen_inline_result()
async def edit_inline_result(client, result):
    await inline_result_handler(result, bot)

@bot.on_callback_query()
async def force_edit_inline_result(client, callback):
    await callback_handler(callback)

@bot.on_message(imdb_filter)
async def imdb(client, message):
    await imdb_handler(message)

@aiocron.crontab('*/30 * * * *')
async def push_rss():
    item_list = rss.fetch()
    for item in item_list:
        await bot.send_message(-1001195256281, item, disable_web_page_preview=True)

bot.run()
