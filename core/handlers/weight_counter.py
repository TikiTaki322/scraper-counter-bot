from aiogram import html

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states_weight import WeightForm
from core.keyboards.reply import get_shipment_type_keyboard, get_try_again_weight_counter_or_menu

from core.utils_algorithms.helvetica_weight_counter_bot_version import get_values_checker, converter_to_list, \
    count_brutto, converter_to_airtable_format


async def get_start_calculation(message: Message, state: FSMContext):
    await message.answer(f'You`ve selected a weight counter. Choose the {html.bold("type of shipment")}:',
                         reply_markup=get_shipment_type_keyboard())
    await state.set_state(WeightForm.GET_SHIPMENT_TYPE)


async def get_shipment_type(message: Message, state: FSMContext):
    if not message.text.startswith('Michael') and not message.text.startswith('Default'):
        await state.clear()
        await message.answer('Push the buttons!', reply_markup=get_try_again_weight_counter_or_menu())
        raise ValueError('Error with type of shipment')

    await message.answer(f'Let me know the number of {html.bold("your current")} box/pallet:')

    global ternary_result
    ternary_result = {2: 'Michael'} if message.text.startswith('Michael') else {1: 'Default'}
    shipment_type = [*ternary_result.keys()][0]
    await state.update_data(shipment_type=shipment_type)
    await state.set_state(WeightForm.GET_BOX_NUMBER)


async def get_box_number(message: Message, state: FSMContext):
    box_number = await get_values_checker(message, state, int)
    await message.answer(f'Enter the {html.bold("factual weight")} of box/pallet #{box_number} (in kg):')
    await state.update_data(box_number=box_number)
    await state.set_state(WeightForm.GET_FACTUAL_WEIGHT)


async def get_factual_weight(message: Message, state: FSMContext):
    factual_weight = await get_values_checker(message, state, float)
    await message.answer(f'Enter {html.bold("netto weights")} for current box/pallet:')
    await state.update_data(factual_weight=factual_weight)
    await state.set_state(WeightForm.GET_NETT_WEIGHT)


async def get_netto_weight(message: Message, state: FSMContext):
    netto_weight = await converter_to_list(message, 'netto weight', state)
    # print(f'Netto_weight: {netto_weight}')
    await state.update_data(netto_weight=netto_weight)
    await state.set_state(WeightForm.GET_QUANTITY)
    await message.answer(f'Enter {html.bold("quantity")} of items for current box/pallet:')


async def get_quantity(message: Message, state: FSMContext):
    quantity = await converter_to_list(message, 'quantity', state)
    # print(f'Quantity: {quantity}')
    await state.update_data(quantity=quantity)

    context_data = await state.get_data()

    shipment_type = context_data.get('shipment_type')
    box_number = context_data.get('box_number')
    factual_weight = context_data.get('factual_weight')
    netto_weight = context_data.get('netto_weight')
    quantity = context_data.get('quantity')

    result = await count_brutto(shipment_type, factual_weight, netto_weight, quantity, message, state)

    user_data = f'Gross weight for the box №{box_number}:\n\n{converter_to_airtable_format(result)}\n\nSum of gross weight: {round(sum(result), 2)}kg\n\n' \
                f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInput data:\r\n' \
                f'Type of shipment: "{ternary_result.get(shipment_type)}"\r\n' \
                f'Factual box weight: {factual_weight}kg\r\n' \
                f'Netto weight: {netto_weight}\r\n' \
                f'Quantity: {quantity}'

    await message.answer(user_data, reply_markup=get_try_again_weight_counter_or_menu())
    await state.clear()


