from loguru import logger
from app.repository.account_telethon import AccountRepository
from app.repository.channel import ChannelRepository
from typing import Any
from pyrogram import Client


class AccountService:

    def __init__(self,
                 repository_account_telethon: AccountRepository,
                 repository_channel: ChannelRepository):
        self._repository_account_telethon = repository_account_telethon
        self._repository_channel = repository_channel

    async def get(self, phone: str = None, id: int = None):
        if phone is not None and id is not None:
            raise ValueError(
                "Both phone and id cannot be specified at the same time")
        if phone:
            return self._repository_account_telethon.get(phone_number=phone)
        elif id:
            return self._repository_account_telethon.get(id=id)
        else:
            raise ValueError("Either phone or id must be specified")

    async def get_or_create(self, obj_in: Any):

        if isinstance(obj_in, dict):
            account = self._repository_account_telethon.get(
                phone_number=obj_in.get("phone_number"))
            if account is not None:
                return account
            async with Client(str(obj_in.get('api_id')), obj_in.get('api_id'),
                              obj_in.get('api_hash')) as client:
                string_session = await client.export_session_string()
                logger.warning('Тут')

            return self._repository_account_telethon.create(obj_in=obj_in | {
                'api_id': obj_in.get('api_id'),
                'api_hash': obj_in.get('api_hash'),
                'session': string_session},
                commit=True)

        return self._repository_account_telethon.get(phone_number=obj_in)

    async def list(self):
        return self._repository_account_telethon.list()
