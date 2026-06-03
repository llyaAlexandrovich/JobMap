import asyncio, logging, os
from configparser import ConfigParser


from loader import *
from handlers import admin, user, common
from handlers.admin import vacancy_data_handlers
from utils.middleware.status import AdminMiddleware
from tables.database import init_asessions


async def on_startup():
    logging.info("Initializing DB sessions")
    init_asessions()

    logging.info("Getting bot default properties")
    bot_info = await dp.get("bot").get_me()
    logging.info(f"Bot name is now: {bot_info.username}")

    logging.info("Loading external env")
    config = ConfigParser()
    config.read("providers.ini", "utf-8")

    # Data providers.

    # 1837bc2c546d46c705204cf9
    os.environ["DATAPROVIDER_NAME_1837bc2c546d46c705204cf9"] = config["1837bc2c546d46c705204cf9"]["DATAPROVIDER_NAME"]
    os.environ["DATAPROVIDER_LINK_1837bc2c546d46c705204cf9"] = config["1837bc2c546d46c705204cf9"]["DATAPROVIDER_LINK"]


async def main():
    try:
        logging.info("Initialization")
        await on_startup()

        logging.info("Setting up the middleware")
        dp.message.middleware(AdminMiddleware())
        dp.callback_query.middleware(AdminMiddleware())

        logging.info("Setting up routers")
        dp.include_routers(admin.admin_handler.router,
                           vacancy_data_handlers.data_handler_1837bc2c546d46c705204cf9.router,
                           common.common_handler.router
                           )

        logging.info("Starting polling")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if "__main__" == __name__:
    asyncio.run(main());
