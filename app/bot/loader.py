import os
import logging
import enum


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    handlers=[logging.FileHandler("global.log", encoding="utf-8")]
)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


if TELEGRAM_BOT_TOKEN != None:
    bot = Bot(TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    class AdminButtons(enum.Enum):
        send_vacancy = "Send vacancy"

    ADMIN_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=item.value, callback_data=item.name)] for item in AdminButtons
        ]
    )
else:
    logging.error("Bot loading error: bot token is invalid")
