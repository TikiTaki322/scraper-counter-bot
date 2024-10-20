from aiogram.fsm.state import StatesGroup, State


class WeightForm(StatesGroup):
    GET_SHIPMENT_TYPE = State()
    GET_BOX_NUMBER = State()
    GET_FACTUAL_WEIGHT = State()
    GET_NETT_WEIGHT = State()
    GET_QUANTITY = State()

