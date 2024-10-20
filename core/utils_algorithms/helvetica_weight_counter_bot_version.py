import sys
import asyncio

from aiogram import html
from aiogram.types import Message

from pprint import pprint
from random import randint

from core.keyboards.reply import get_try_again_weight_counter_or_menu


async def get_values_checker(message, state, int_or_float):
    try:
        value = int_or_float(message.text)
    except ValueError:
        await message.answer(f'Acceptable only digits. Try again', reply_markup=get_try_again_weight_counter_or_menu())
        await state.clear()
        raise ValueError('Only digits acceptable..')
    else:
        return value


async def quant_weight_length_validation(quant, weight_value, message, state):
    if len(quant) != len(weight_value):
        await message.answer(
            'The length of the quantity values does not equal to the length of the weight values, please try again.',
            reply_markup=get_try_again_weight_counter_or_menu())
        await state.clear()
        raise TypeError('The length of the quantity values does not equal to the length of the weight values, try again.')


async def print_netto_of_all(netto_of_all, message):
    await message.answer(f'Nett weight multiplied by the quantity:\n\n{converter_to_airtable_format(netto_of_all)}\n\n')


def converter_to_airtable_format(variable):
    temp = '\n'.join(map(str, variable))
    return temp


async def converter_to_list(message, log_text, state):
    result = []
    for i in message.text.split():
        try:
            result.append(float(i))
        except ValueError:
            await message.answer(
                'You should input only digits : 0.2, 9, 134, 23.5, 2.55 etc',
                reply_markup=get_try_again_weight_counter_or_menu())

            await state.clear()
            raise ValueError()

    await message.answer(f'Your {html.bold(log_text)} values were successfully processed.\n')
    return result


def get_weight_of_all(weight_of_one, quantity, rounding_value=2):
    weight_of_all = [round(i*j, rounding_value) for i, j in zip(weight_of_one, quantity)]
    return weight_of_all


def get_michael_brutto_of_one(netto_of_one):
    brutto_of_one = list(map(lambda x: x+0.100, netto_of_one))
    return brutto_of_one


def index_generator(collection):
    dict_collection = dict(enumerate(collection))
    sorted_dict_collection = dict(sorted(dict_collection.items(), key=lambda x: x[1]))

    for k, v in sorted_dict_collection.items():
        yield k, v


async def checker_michael_brutto(message, brutto_of_all, brutto_of_one, factual_weight, quant, generator_func=None, flag=False):
    sum_of_brutto = round(sum(brutto_of_all), 1)
    # print(f'Sum of brutto in checker_michael_brutto(): {sum_of_brutto}')

    if sum_of_brutto > factual_weight:
        await message.answer(f'Summ of brutto multiplied on quantity greater then factual weight.\nFactual -> {factual_weight}kg, Summ of brutto -> {sum_of_brutto}kg.\n')
        # print(f'Brutto of one: {brutto_of_one}')
        return brutto_of_one

    elif sum_of_brutto < factual_weight:
        if flag:
            await message.answer(f'Summ of brutto multiplied on quantity less then factual weight.\nFactual -> {factual_weight}kg, Summ of brutto -> {sum_of_brutto}kg.\n')
        try:
            index = next(generator_func)[0]
            brutto_of_one[index] = round(brutto_of_one[index] + 0.100, 1)
            brutto_of_all = get_weight_of_all(brutto_of_one, quant, 1)
        except StopIteration:
            generator_func.close()
            generator_func = index_generator(quant)
        finally:
            if len(quant) != 1:
                return await checker_michael_brutto(message, brutto_of_all, brutto_of_one, factual_weight, quant, generator_func)
            else:
                # print(f'Brutto of one: {brutto_of_one}')
                return brutto_of_one

    else:
        await message.answer(f'Summ of brutto multiplied on quantity is equal to factual weight.\nFactual -> {factual_weight}kg, Summ of brutto -> {sum_of_brutto}kg.\n')
        # print(f'Brutto of one: {brutto_of_one}')
        return brutto_of_one


async def count_brutto(shipment_type, factual_weight, netto_of_one, quant, message, state):
    await quant_weight_length_validation(quant, netto_of_one, message, state)

    if shipment_type == 1:
        netto_of_all = get_weight_of_all(netto_of_one, quant)
        await print_netto_of_all(netto_of_all, message)
        result = list(map(lambda x: round((x*factual_weight)/sum(netto_of_all), 2), netto_of_all))
    else:
        brutto_of_one = get_michael_brutto_of_one(netto_of_one)
        brutto_of_all = get_weight_of_all(brutto_of_one, quant, 1)
        result = await checker_michael_brutto(message, brutto_of_all, brutto_of_one, factual_weight, quant, index_generator(quant), True)

    return result

