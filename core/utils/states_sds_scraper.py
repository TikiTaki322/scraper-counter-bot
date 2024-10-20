from aiogram.fsm.state import StatesGroup, State


class SdsForm(StatesGroup):
    GET_SOURCE = State()
    GET_CATALOG_VALUE = State()