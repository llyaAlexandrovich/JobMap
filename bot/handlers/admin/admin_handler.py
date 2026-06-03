import asyncio


from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext


from loader import *
from utils.controls.control_input import VacancyData


router = Router()


@router.message(Command("admin"), flags={"is_admin": True})
async def admin(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="You're admin!",
        reply_markup=ADMIN_KEYBOARD)


@router.message(F.text == "Send vacancy", flags={"is_admin": True})
async def start_vacancies_polling_loop(message: Message, state: FSMContext):
    await state.set_state(VacancyData.auto_vacancy)
    
    await message.answer(
        "Send me vacancies to add",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Cancel", callback_data="back_to_admin")],
                ]
        )
    )


@router.callback_query(F.data == "back_to_admin", flags={"is_admin": True})
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Back to admin menu",
        reply_markup=ADMIN_KEYBOARD
    )
