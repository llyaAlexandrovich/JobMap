from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from aiogram.dispatcher.event.handler import HandlerObject

from sqlalchemy import select
from tables import async_session
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


        async with async_session() as session:
            result = await session.execute(
                select(User).filter(User.id == user.id)
            )
            db_user = result.scalar_one_or_none()


        if db_user and db_user.admin:
            data["db_user"] = db_user
            return await handler(event, data)
        return None
