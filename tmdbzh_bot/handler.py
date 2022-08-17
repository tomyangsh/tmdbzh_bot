import re
import requests

from .util import build_inline_answer, build_message, Inline_search_markup

from pyrogram import enums

async def inline_handler(inline_query):
    query = inline_query.query
    answer = build_inline_answer(query)
    await inline_query.answer(answer)

async def inline_result_handler(result, bot):
    match = re.match('(\w+)-(\d+)', result.result_id)
    type = match.group(1)
    id = match.group(2)
    text = build_message(type, id)
    await bot.edit_inline_text(result.inline_message_id, text)

async def callback_handler(callback):
    await callback.answer("wait")
    match = re.match('(\w+)-(\d+)', callback.data)
    type = match.group(1)
    id = match.group(2)
    text = build_message(type, id)
    await callback.edit_message_text(text)

async def start_handler(message, bot):
    me = await bot.get_me()
    if message.chat.type == enums.ChatType.PRIVATE or re.search(me.username, message.text):
        await message.reply_text("TMDb 影视及人物信息检索", reply_markup=Inline_search_markup)

async def imdb_handler(message):
    await bot.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
    type = "movie"
    id = message.text
    result = build_message(type, id, imdb=True)
    text = result['text']
    img = result['img']
    if img:
        await message.reply_photo(img, caption=text)
    else:
        await message.reply_text(text)
