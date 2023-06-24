from app.core.containers import Container
import asyncio
from utils import register_telethon_account
from telegram_sender_bot.handlers import telethon_handlers
from telegram_sender_bot.bot import main
from telegram_sender_bot.handlers import user_handlers

if __name__ == '__main__':
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[register_telethon_account,
                            user_handlers, telethon_handlers])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register_telethon_account.register())
    tasks = [
        loop.create_task(telethon_handlers.start()),
        loop.create_task(main())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
