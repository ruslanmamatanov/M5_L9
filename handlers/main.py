import asyncio
import logging
import sys
from aiogram.enums import ParseMode
from handlers.cmd_handlers import cmd_router
from handlers.msg_handlers import msg_router
from aiogram import Bot, Dispatcher
from config import TOKEN as t
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=t, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(cmd_router, msg_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")