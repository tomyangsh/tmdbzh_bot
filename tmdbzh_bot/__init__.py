import tomli

from pyrogram import Client

with open("config.toml", "rb") as f:
    CONFIG = tomli.load(f)
