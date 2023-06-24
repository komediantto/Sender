import json
from loguru import logger
from dependency_injector.wiring import inject, Provide
from app.services.account_telethon import AccountService
from app.services.spamsettings import SpamSettingsService
from app.core.containers import Container


@inject
async def register(account_service: AccountService = Provide[
                                        Container.account_telethon_service],
                   spam_settings: SpamSettingsService = Provide[
                                        Container.spam_settings_service]):
    with open('cred.json', 'r') as file:
        data = json.load(file)

    for k, v in data.items():
        phone = v['phone']
        api_id = v['api_id']
        api_hash = v['api_hash']
        await account_service.get_or_create(obj_in={'phone_number': phone,
                                                    'api_id': api_id,
                                                    'api_hash': api_hash})
    await spam_settings.get_or_create(obj_in={'id': 1})
    logger.warning('Настройки установлены')
