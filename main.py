import asyncio
import asyncpg
import logging

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from core.handlers.basic import get_start, get_media, get_hello, get_echo, get_dice, get_menu, get_users

from core.handlers import weight_counter, sds_scraper

from core.utils.states_weight import WeightForm
from core.utils.states_sds_scraper import SdsForm

from core.utils.commands import set_commands
from core.utils.dbinitialization import create_db, create_table
from core.settings import settings

from core.middlewares.dbmiddleware import DbSession

from aiogram.fsm.storage.redis import RedisStorage


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text=f'Bot is running, {html.bold("mr. Creator")}')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text=f'Bot is terminated, {html.bold("mr. Creator")}')


async def create_pool():
    return await asyncpg.create_pool(user=settings.bots.db_user, password=settings.bots.db_password,
                                     database=settings.bots.db_name,
                                     host=settings.bots.host, port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                        )
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    create_db()
    create_table()

    pool_connect = await create_pool()
    storage = RedisStorage.from_url(f'redis://{settings.bots.host}:6379/0')

    dp = Dispatcher(storage=storage)
    dp.update.middleware.register(DbSession(pool_connect))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(weight_counter.get_start_calculation, F.text.lower().in_({'another one try', '/weight', 'weight count'}))
    dp.message.register(weight_counter.get_shipment_type, WeightForm.GET_SHIPMENT_TYPE)
    dp.message.register(weight_counter.get_box_number, WeightForm.GET_BOX_NUMBER)
    dp.message.register(weight_counter.get_factual_weight, WeightForm.GET_FACTUAL_WEIGHT)
    dp.message.register(weight_counter.get_netto_weight, WeightForm.GET_NETT_WEIGHT)
    dp.message.register(weight_counter.get_quantity, WeightForm.GET_QUANTITY)

    dp.message.register(sds_scraper.get_start_sds_scraper, F.text.lower().in_({'try again', '/search', 'sds search'}))
    dp.message.register(sds_scraper.get_source_value, SdsForm.GET_SOURCE)
    dp.message.register(sds_scraper.get_catalog_value, SdsForm.GET_CATALOG_VALUE)

    dp.message.register(get_dice, F.text.lower().in_({'dice me', '/dice', 'dice again'}))

    dp.message.register(get_media, F.photo | F.animation | F.video)
    dp.message.register(get_hello, F.text.lower().startswith('hi') | F.text.lower().startswith('hello'))

    dp.message.register(get_start, F.text.lower().in_({'/start'}))
    dp.message.register(get_menu, F.text.lower().in_({'/menu', 'back to menu'}))
    dp.message.register(get_users, F.from_user.id.in_({settings.bots.admin_id}) & F.text.lower() == 'users')
    dp.message.register(get_echo, F.text)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Program was finished by keyboard interrupt')
