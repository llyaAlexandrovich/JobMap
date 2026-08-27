import os, logging, enum, asyncio, uvloop


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import BasicAuth

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

try:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d.%m.%Y %X:%z",
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

    auth = BasicAuth(login=os.getenv("PROXY_LOGIN"), password=os.getenv("PROXY_PASSWORD"))
    session = AiohttpSession(proxy=("http://" + os.getenv("PROXY_IP") + ':' + os.getenv("PROXY_PORT"), auth))

    bot = Bot(TELEGRAM_BOT_TOKEN, session=session)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    ADMIN_KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=item.value)] for item in AdminButtons
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

except Exception as e:
    logging.fatal(f"Loader error: {e}")
