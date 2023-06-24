from dependency_injector.wiring import inject, Provide
from app.services.account_telethon import AccountService
from app.core.containers import Container
from app.core.config import settings as stg
from loguru import logger
from pyrogram import Client, filters, idle, compose
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from telegram_sender_bot.bot import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.telegram_sender_bot.handlers.user_handlers import IdCallbackFactory
import re
import uvloop

uvloop.install()


async def callback(client: Client, message: Message):
    logger.warning(message.text)
    await client.get_chat(stg.GROUP)
    chat_participants = []
    async for member in client.get_chat_members(stg.GROUP):
        chat_participants.append(member)
    users_id = [participant.user.id for participant in chat_participants]
    logger.warning(users_id)
    sender = message.from_user
    logger.warning(sender.id)
    if sender.id == stg.BOT_ID:
        logger.warning(message.text)
        user_message = re.search(r'\s(.*)', message.text).group()
        try:
            user_id = int(
                re.search(r'^\S+', message.text).group())
            logger.warning(user_id)
            await client.send_message(user_id, user_message)
        except Exception as e:
            logger.error(f'Не юзер, либо вот эта ошибка: {e}')
    elif sender.id in users_id:
        me = await client.get_me()
        if sender.id != me.id:
            logger.info(me.phone_number)
            logger.warning(sender.username)
            user_url = f'https://t.me/{sender.username}'
            text = f'{message.text} - {user_url}'
            builder = InlineKeyboardBuilder()
            builder.button(
                text="Отправить сообщение",
                callback_data=IdCallbackFactory(user_id=sender.id,
                                                acc_id=me.id))
            await bot.send_message(stg.ADMIN_ID,
                                   text=text,
                                   reply_markup=builder.as_markup())
            logger.info(text)
    else:
        logger.warning('Мимо')


@inject
async def start(account_service: AccountService = Provide[
                Container.account_telethon_service]):
    clients = []
    accs = await account_service.list()
    logger.warning(accs)

    for i, acc in enumerate(accs):
        client = Client(name=f'Client №{i}', session_string=acc.session)
        clients.append(client)
    logger.warning(clients)

    for client in clients:
        client.add_handler(MessageHandler(callback, filters.private))
        logger.warning('Хэндлер добавлен')

    await compose(clients)
    await idle()
