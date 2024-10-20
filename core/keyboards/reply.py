from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Weight count')
    keyboard_builder.button(text='SDS search')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_echo_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Back to menu')
    keyboard_builder.button(text='Dice me')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_dice_or_menu():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Back to menu')
    keyboard_builder.button(text='Dice again')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_shipment_type_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Default shipment (minimal netto is 0.010 grams)')
    keyboard_builder.button(text='Michael shipment (minimal netto is 0.100 grams)')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_try_again_weight_counter_or_menu():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Back to menu')
    keyboard_builder.button(text='Another one try')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_source_selection_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Sigma')
    keyboard_builder.button(text='Cymitquimica', description='Do you see me?')
    keyboard_builder.button(text='USP')
    keyboard_builder.button(text='Abcam')
    keyboard_builder.button(text='TCI')
    keyboard_builder.button(text='TRC')
    keyboard_builder.button(text='Progen')
    keyboard_builder.button(text='Honeywell')
    keyboard_builder.button(text='Aniara')
    keyboard_builder.button(text='Biorad')
    keyboard_builder.button(text='EDQM')
    keyboard_builder.button(text='Chemicalsafety')
    keyboard_builder.button(text='VWR')
    keyboard_builder.button(text='Bdbiosciences')
    keyboard_builder.adjust(3, 3, 3, 3, 2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_try_again_sds_parser_or_menu():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Back to menu')
    keyboard_builder.button(text='Try again')
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)