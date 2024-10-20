from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start of work'
        ),
        BotCommand(
            command='menu',
            description='Go to menu'
        ),
        BotCommand(
            command='weight',
            description='Calculate weight'
        ),
        BotCommand(
            command='search',
            description='Search the SDS document'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
