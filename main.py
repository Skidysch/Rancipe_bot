import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from core.handlers.basic import start_command, shuffle_command, reshuffle_command
from core.middlewares.dbmiddleware import DBSession
from core.utils.commands import set_commands
from core.settings import settings


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bot.admin_id, text='Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bot.admin_id, text='Bot stopped!')


def create_pool() -> asyncpg.pool.Pool:
    return asyncpg.create_pool(user=settings.db.db_user, password=settings.db.db_pass,
                               database=settings.db.db_name,
                               host=settings.db.db_host, port=settings.db.db_port,
                               command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(token=settings.bot.bot_token)
    dp = Dispatcher()
    pool_connect = await create_pool()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.update.middleware.register(DBSession(pool_connect))

    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(shuffle_command, Command(commands='shuffle'))
    dp.callback_query.register(shuffle_command, F.data == 'shuffle')
    dp.callback_query.register(reshuffle_command, F.data == 'reshuffle')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
