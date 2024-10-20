from aiogram import html

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states_sds_scraper import SdsForm
from core.utils_algorithms.sds_scraper_bot_version import sds_search, source_checker, sigma_parse, cymitquimica_parse, \
    usp_parse, abcam_parse, tci_parse, trc_parse, progen_parse, honeywell_parse, aniara_parse, biorad_parse, edqm_parse, \
    chemicalsafety_parse, vwr_parse, bdbiosciences_parse
from core.keyboards.reply import get_source_selection_keyboard, get_try_again_sds_parser_or_menu


async def get_start_sds_scraper(message: Message, state: FSMContext):
    await message.answer(f'You`ve selected a SDS parser. Choose the {html.bold("search source")}:',
                         reply_markup=get_source_selection_keyboard())
    await state.set_state(SdsForm.GET_SOURCE)


async def get_source_value(message: Message, state: FSMContext):
    try:
        source_name, index, link = await source_checker(message)
    except TypeError as e:
        print(
            f'User: {message.from_user.first_name}, ID: {message.from_user.id}, (TypeError) Error message from get_source_value\n', \
            f'(User does not use the button selection):\n{e}')
        await state.clear()
    else:
        await state.update_data(source_name=source_name)
        await state.update_data(index=index)
        await state.update_data(link=link)

        if source_name.lower().startswith('chemicalsafety'):
            await message.answer(
                f'Selected source is {html.bold(source_name)}.\r\n\r\nIt is an universal source so enter the {html.bold("product name")} instead of catalog number:')
        else:
            await message.answer(f'Selected source is {html.bold(source_name)}.\r\n\r\nEnter the {html.bold("catalog number")}:')
        await state.set_state(SdsForm.GET_CATALOG_VALUE)


async def get_catalog_value(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        await message.answer('Input error', reply_markup=get_try_again_sds_parser_or_menu())
        await state.clear()
    else:
        catalog_number = message.text
        await message.answer(f'Searching for an item {html.bold(catalog_number)}.')
        await state.update_data(catalog_number=catalog_number)

        context_data = await state.get_data()
        source_name = context_data.get('source_name')
        index = context_data.get('index')
        link = context_data.get('link')
        catalog_number = context_data.get('catalog_number')

        functions_db = [sigma_parse, cymitquimica_parse, usp_parse, abcam_parse, tci_parse, trc_parse, progen_parse,
                        honeywell_parse, aniara_parse, biorad_parse, edqm_parse,
                        chemicalsafety_parse, vwr_parse, bdbiosciences_parse]
        func_name = functions_db[index]

        result = await sds_search(message, source_name, func_name, link, catalog_number)
        if result is not None:
            user_data = f'Result from the {html.bold(source_name)}:\r\n\r\n{html.bold(result)}'
            await message.answer(user_data, reply_markup=get_try_again_sds_parser_or_menu())
        await state.clear()
