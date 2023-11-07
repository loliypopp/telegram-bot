import psycopg2 as sql
import asyncio

from aiogram import Bot, Dispatcher
from handlers import bot_messages, user_commands




async def main():
    token = '6727496119:AAF5io_NA4HU6E79N7epHJaCOCm66n3hZxc'
    bot = Bot(token, parse_mode="HTML")
    dp = Dispatcher()
    
    dp.include_routers(
        user_commands.router,
        bot_messages.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())