import asyncio


from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


from loader import *
from tables.database import get_db_asession
from tables.models import User, SpatialInfo, ProvidersInfo, Vacancy
from utils.controls.control_input import VacancyData


router = Router()


@router.message(VacancyData.vacancy, flags={"is_admin": True})
async def get_vacancy_data(message: Message, state: FSMContext):
    async with await get_db_asession("bot") as session:
        async with session.begin():
            provider_name = "wtf"
            strings = message.text.split('\n')
            if strings[0].find('🟢'):
                strings[0].replace('🟢', ' ').replace(' ', '')
            if strings[1].find('🏢'):
                strings[1].replace('🏢', ' ').replace(' ', '')
            tags = strings[2].split(' ')

            
