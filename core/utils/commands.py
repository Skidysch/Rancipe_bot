from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description="Let's go!"
        ),
        BotCommand(
            command='shuffle',
            description='Generate random recipe'
        ),

    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
