import tomli
import os

from pyrogram import Client

if not os.path.exists("config.toml"):
    print("请复制config-sample.toml为config.toml并修改")
    exit()

with open("config.toml", "rb") as f:
    CONFIG = tomli.load(f)

bot = Client(**CONFIG["telegram"])
