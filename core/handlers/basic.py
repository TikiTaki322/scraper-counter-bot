from random import randint

from aiogram import Bot, html
from aiogram.types import Message
from core.keyboards.reply import get_menu_keyboard, get_echo_reply_keyboard, get_dice_or_menu
from core.utils.dbconnect import Request


async def get_start(message: Message, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(
        f'Welcome {html.bold(message.from_user.first_name)}, glad to see you here!\nThis bot can search SDS documents and count weight for shipment, pick what you want:',
        reply_markup=get_menu_keyboard())


async def get_users(message: Message, request: Request):
    result = await request.show_data()
    await message.answer(f'Hello Mr.admin, all info here:\n\n{result}')


async def get_menu(message: Message):
    await message.answer(f'Nice to see you again! Select the {html.bold("desired action")}:',
                         reply_markup=get_menu_keyboard())


async def get_echo(message: Message):
    await message.answer(f'{html.bold(message.text[::-1])}\nTry to use buttons.',
                         reply_markup=get_echo_reply_keyboard())


async def get_dice(message: Message):
    await message.answer(f'Human, your value: {html.bold(randint(0, message.from_user.id))}',
                         reply_markup=get_dice_or_menu())


async def get_media(message: Message):
    await message.answer(html.bold('You`ve send the media content. Don`t do it!'))


async def get_hello(message: Message):
    await message.answer('Hello to you too!')