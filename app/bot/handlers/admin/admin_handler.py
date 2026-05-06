import asyncio


from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from loader import *
from utils.controls.control_input import VacancyData


router = Router()


@router.message(Command("admin"), flags={"is_admin": True})
async def admin(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="You're admin!")


@router.callback_query(F.data == AdminButtons.send_vacancy.name, flags={"is_admin": True})
async def start_polling_loop(callback: CallbackQuery, state: FSMContext):
    await state.set_state(VacancyData.vacancy)
    
    await bot.send_message(
        callback.message.chat.id,
        "Send me vacancies to add",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Cancel", callback_data="back_to_admin")],
                ]
        )
    )
