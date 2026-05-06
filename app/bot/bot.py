import asyncio
import logging


from loader import *
from handlers import admin, user, common, dp
from utils.middleware.status import AdminMiddleware
from tables.database import get_db_asession, init_asessions


async def on_startup():
    logging.info("Initializing DB sessions")
    init_asessions()

    logging.info("Getting bot default properties")
    bot_info = await dp.get("bot").get_me()
    logging.info(f"Bot name is now: {bot_info.username}")


async def main():
    try:
        logging.info("Calling on_starpup functionality")
        await on_startup()

        logging.info("Setting up the middleware")
        dp.message.middleware(AdminMiddleware())
        dp.callback_query.middleware(AdminMiddleware())

        logging.info("Setting up routers")
        dp.include_routers(admin.admin_handler.router, common.common_handler.router)

        logging.info("Starting polling")
        await dp.start_polling(bot)
    finally:
        logging.info("Stopping polling")
        await bot.session.close()


if "__main__" == __name__:
    logging.basicConfig(
        filename="./log/bot/log.log",
        filemode='a',
        format="[%(asctime)s] %(message)s",
        datefmt="%x %X:%z",
        level=logging.INFO,
        handlers=[logging.FileHandler("./log/bot/log.log", 'a', "utf-8"),],
        encoding="utf-8"
    )

    asyncio.run(main());
