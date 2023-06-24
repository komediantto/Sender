from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from telegram_sender_bot import bot

from aiogram.types import Message, ChatMemberUpdated
from dependency_injector.wiring import inject, Provide
from app.services.spamsettings import SpamSettingsService
from app.core.containers import Container
from app.core.config import settings
from loguru import logger
from aiogram.filters import Command, Text
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER


from services.account_telethon import AccountService
from aiogram.filters.callback_data import CallbackData
from app.telegram_sender_bot.keyboards.stngs_kbd import stngs_kbd
from pyrogram import Client


router: Router = Router()
router.chat_member.filter(F.chat.id == settings.GROUP)


class IdCallbackFactory(CallbackData, prefix="sender"):
    user_id: str
    acc_id: int


class BaseStates(StatesGroup):
    waiting_for_message = State()


class SettingsState(StatesGroup):
    choose = State()
    delay = State()
    template = State()
    limit = State()


@router.message(Command('settings'))
async def choice(message: Message, state: FSMContext):
    await state.set_state(SettingsState.choose)
    await message.answer('Выберите пункт настройки:', reply_markup=stngs_kbd())


@router.callback_query(Text('delay'), SettingsState.choose)
async def delay(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новое время задержки в секундах')
    await state.set_state(SettingsState.delay)


@router.message(SettingsState.delay)
@inject
async def set_delay(message: types.Message,
                    state: FSMContext,
                    spam_settings_service: SpamSettingsService = Provide[
                        Container.spam_settings_service]):
    try:
        new_delay = int(message.text)
        await spam_settings_service.update(id=1, obj_in={'delay': new_delay})
        await message.answer(f'Новое время задержки: {new_delay}')
        await state.clear()
    except Exception:
        await message.answer('Введите число в секундах')
        await state.set_state(SettingsState.delay)


@router.callback_query(Text('hello_message'), SettingsState.choose)
async def hello_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новое приветственное сообщение:')
    await state.set_state(SettingsState.template)


@router.message(SettingsState.template)
@inject
async def set_hello(message: types.Message,
                    state: FSMContext,
                    spam_settings_service: SpamSettingsService = Provide[
                        Container.spam_settings_service]):
    new_template = str(message.text)
    await spam_settings_service.update(id=1,
                                       obj_in={
                                           'template_message': new_template})
    await message.answer(f'Новое приветственное сообщение: {new_template}')
    await state.clear()


@router.callback_query(Text('hello_limit'), SettingsState.choose)
async def limit(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новый лимит приветствий:')
    await state.set_state(SettingsState.limit)


@router.message(SettingsState.limit)
@inject
async def set_limit(message: types.Message,
                    state: FSMContext,
                    spam_settings_service: SpamSettingsService = Provide[
                        Container.spam_settings_service]):
    try:
        new_limit = int(message.text)
        await spam_settings_service.update(id=1, obj_in={
            'dialog_limit': new_limit})
        await message.answer(f'Новый лимит приветствий: {new_limit}')
        await state.clear()
    except Exception:
        await message.answer('Введите число:')
        await state.set_state(SettingsState.limit)


@router.callback_query(IdCallbackFactory.filter())
async def process_message(callback: types.CallbackQuery,
                          callback_data: IdCallbackFactory,
                          state: FSMContext):
    await state.update_data({'user_id': callback_data.user_id,
                             'acc_id': callback_data.acc_id})
    await state.set_state(BaseStates.waiting_for_message)
    await callback.answer()


@router.message(BaseStates.waiting_for_message)
@inject
async def process_client_connection(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.bot.send_message(data['acc_id'],
                               (data['user_id'] + ' ' + message.text))
    await state.clear()


COUNT = 0
current_client_index = 0


@router.chat_member(ChatMemberUpdatedFilter(
    member_status_changed=IS_NOT_MEMBER >> MEMBER
))
@inject
async def new_chat_member(event: ChatMemberUpdated, bot: Bot,
                          account_service: AccountService = Provide[
                              Container.account_telethon_service],
                          spam_settings_service: SpamSettingsService = Provide[
                              Container.spam_settings_service]):
    global COUNT, current_client_index
    logger.warning(event)
    settings = spam_settings_service.get(id=1)
    accs = await account_service.list()
    try:
        acc = accs[current_client_index]
    except IndexError:
        current_client_index = 0
        acc = accs[current_client_index]
    async with Client(name=f'Client №{current_client_index}',
                      session_string=acc.session) as client:
        await client.send_message(event.new_chat_member.user.id,
                                  settings.template_message)
    COUNT += 1
    message_limit = settings.dialog_limit

    if COUNT == message_limit:
        COUNT = 0
        current_client_index = current_client_index + 1
