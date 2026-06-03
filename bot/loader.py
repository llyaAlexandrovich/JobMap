import os
import logging
import enum


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%x %X:%z",
    level=logging.INFO,
    handlers=[logging.FileHandler("/log/log.txt", 'a', "utf-8"), logging.StreamHandler()],
    encoding="utf-8"
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class AdminButtons(enum.Enum):
        send_vacancy = "Send vacancy"

if not TELEGRAM_BOT_TOKEN:
    logging.error("Bot loading error: bot token is invalid, unbound or other way inaccessible")
    while True:
        pass

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

ADMIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=item.value)] for item in AdminButtons
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
