import os
from hashlib import sha3_512
from geopy import Nominatim
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


from loader import *
from tables.transactions import create_new_vacancy_transaction
from utils.controls.control_input import VacancyData


router = Router()


@router.message(VacancyData.auto_vacancy, flags={"is_admin": True})
async def get_vacancy_data_auto(message: Message, state: FSMContext):
    # If there's no message exception will be thrown.
    # Checking for that.
    if not message.text:
        await state.clear()
        await message.answer("Send valid message")
        return

    try:
        # Getting data provider.
        provider_name = os.environ.get("DATAPROVIDER_NAME_1837bc2c546d46c705204cf9")
        strings = message.text.split('\n')

        # Validating message.
        if len(strings) < 3:
            await state.clear()
            await message.answer("Unsupported provider or message was corrupted")
            return

        # Safe way to get link to the vacancy.
        vacancy_link = None
        if message.entities:
            for entity in message.entities:
                if entity.type == "text_link":
                    vacancy_link = entity.url
                    break
                elif entity.type == "url":
                    vacancy_link = entity.extract_from(message.text)
                    break

        if not vacancy_link:
            await message.answer("Link was not found in the given message")
            logging.warning(f"Link was not found in the given message: message_id_{message.message_id}")
            return

        vacancy_name=strings[0][2:]
        vacancy_info=strings[1].split('·')
        vacancy_info[0] = vacancy_info[0][2:]
        vacancy_info[1] = vacancy_info[1][2:]
        provider_link=os.environ.get("DATAPROVIDER_LINK_1837bc2c546d46c705204cf9")
        tags_array=[tag.strip() for tag in strings[2].replace('#', '').split(' ') if tag.strip()]
        hash=sha3_512(f"{message.text}{provider_name}".encode()).hexdigest()


        # Getting coordinates using given location name or fallback
        # to the manual coordinates input.
        geolocator = Nominatim(user_agent=os.getenv("USER_AGENT"))
        location = geolocator.geocode(vacancy_info[1], timeout=10)
        if not location:
            # Updating states.
            await state.update_data(
                vacancy_link=vacancy_link,
                vacancy_name=vacancy_name,
                company_name=vacancy_info[0],
                location_name=vacancy_info[1],
                provider_name=provider_name,
                provider_link=provider_link,
                tags_array=tags_array,
                hash=hash
            )

            await message.answer("Error occurred while trying to get required location. Please enter coordinates manually")
            await state.set_state(VacancyData.manual_vacancy)
            return

        location_name = location.address
        geom = from_shape(Point(location.longitude, location.latitude), srid=4326)
        coords = [location.longitude, location.latitude]


        # Some logging for new vacancy.
        log_text = f"""New vacancy info -
            Name: {vacancy_name}
            Location: {location_name}
            Coords: {coords[0]}x{coords[1]}
            Company: {vacancy_info[0]}
            Tags: {tags_array}
        """

        await message.answer(log_text)
        logging.info(log_text)

        # Executing a DB transaction.
        transaction_result = await create_new_vacancy_transaction(
            provider_name = provider_name,
            provider_link = provider_link,
            vacancy_name  = vacancy_name,
            vacancy_link  = vacancy_link,
            tags_array    = tags_array,
            hash          = hash,
            location_name = location_name,
            company_name  = vacancy_name[0],
            geom          = geom
        )

        # Checking for transaction status.
        await message.answer(f"Transaction status: {'Succeeded' if transaction_result else 'Failed'}")
        await state.clear()
        await state.set_state(VacancyData.auto_vacancy)

    except Exception as e:
        logging.error(f"Vacancy data handler error in data_handler_1837bc2c546d46c705204cf9.get_vacancy_data_auto: {e}")
        await state.set_state(VacancyData.manual_vacancy)



@router.message(VacancyData.manual_vacancy, flags={"is_admin": True})
async def get_vacancy_data_manual(message: Message, state: FSMContext):
    if not message.text:
        await state.clear()
        await message.answer("Send valid message")
        return

    try:
        user_input = message.text.replace('\n', '').split(' ')
        geom=from_shape(Point(float(user_input[0]), float(user_input[1])), srid=4326)
        coords=[user_input[0], user_input[1]]

        data = await state.get_data()
        log_text = f"""New vacancy info -
            Name: {data["vacancy_name"]}
            Location: {data["location_name"]}
            Coords: {coords[0]}x{coords[1]}
            Company: {data["company_name"]}
            Tags: {data["tags_array"]}
        """

        await message.answer(log_text)
        logging.info(log_text)


        transaction_result = await create_new_vacancy_transaction(
            provider_name = data["provider_name"],
            provider_link = data["provider_link"],
            vacancy_name  = data["vacancy_name"],
            vacancy_link  = data["vacancy_link"],
            tags_array    = data["tags_array"],
            hash          = data["hash"],
            location_name = data["location_name"],
            company_name  = data["company_name"],
            geom          = geom
        )

        await message.answer(f"Transaction status: {'Succeeded' if transaction_result else 'Failed'}")
        await state.clear()
        await state.set_state(VacancyData.auto_vacancy)

    except Exception as e:
        await state.clear()
        logging.error(f"Vacancy data handler error in data_handler_1837bc2c546d46c705204cf9.get_vacancy_data_manual: {e}")
        await state.set_state(VacancyData.auto_vacancy)
