import re
import requests

from .tmdb import method
from .method import build_message

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, MessageEntity, InputMediaPhoto

IMG_BASE = 'https://oracle.tomyangsh.pw/img'

async def inline_handler(inline_query):
    results = []
    query = inline_query.query
    if not query:
        s = method.discover()
    else:
        s = method.multi_search(query)
    for i in s[:10]:
        if i['year']:
            title = f"{i['name']} ({i['year']}) "
        else:
            title = f"{i['name']} "
        description = i['des'] or ''
        data = f"{i['type']}-{i['id']}"
        url = f"https://www.themoviedb.org/{i['type']}/{i['id']}?language=zh-CN"
        img = f"{IMG_BASE}{i['img']}"
        msg = f"[ㅤ]({img}){title}\n\n{description}ㅤ"
        results.append(InlineQueryResultArticle(title=title, description=description, input_message_content=InputTextMessageContent(msg), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Loading...', url=url)]]), thumb_url=img, id=data))
    await inline_query.answer(results)

async def inline_result_handler(result, bot):
    match = re.match('(\w+)-(\d+)', result.result_id)
    type = match.group(1)
    id = match.group(2)
    text = build_message(type, id)
    await bot.edit_inline_text(result.inline_message_id, text)

async def start_handler(message, bot):
    me = await bot.get_me()
    if message.chat.type != enums.ChatType.PRIVATE and not re.search(me.username, message.text):
        return
    else:
        await message.reply_text("TMDb 影视及人物信息检索", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('点击此处开始搜索', switch_inline_query_current_chat='')]]))

async def imdb_handler(message):
    type = "movie"
    id = message.text
    result = build_message(type, id, imdb=True)
    text = result['text']
    img = result['img']
    if img:
        await message.reply_photo(img, caption=text)
    else:
        await message.reply_text(text)
