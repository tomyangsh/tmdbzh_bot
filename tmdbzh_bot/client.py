from . import CONFIG

from pyrogram import Client

def client(name='bot'):
    _client = Client(**CONFIG["telegram"])
    return _client
