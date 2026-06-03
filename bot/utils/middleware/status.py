from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from aiogram.dispatcher.event.handler import HandlerObject

from sqlalchemy import select
from tables import get_db_asession
from tables.models import User


class AdminMiddleware(BaseMiddleware):
    def __init__(self):
        super(AdminMiddleware, self).__init__()


    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data.get("handler")
        is_admin_required = real_handler.flags.get("is_admin")


        if is_admin_required is None:
            return await handler(event, data)


        user: User = data.get("event_from_user")
        if user is None:
            return None


        session_factory = await get_db_asession("bot")
        if not session_factory:
            return None

        async with session_factory as session:
            result = await session.execute(
                select(User).filter(User.telegram_id == user.id)
            )
            db_user = result.scalar_one_or_none()


        if db_user and db_user.admin:
            data["db_user"] = db_user
            return await handler(event, data)
        return None
