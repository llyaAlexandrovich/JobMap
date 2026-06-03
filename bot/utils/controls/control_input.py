from aiogram.fsm.state import State, StatesGroup



class VacancyData(StatesGroup):
    auto_vacancy = State()
    manual_vacancy = State()
    
