from app.repository.spamsettings import SpamSettings
from typing import Any


class SpamSettingsService:

    def __init__(self, repository_spam_settings: SpamSettings):
        self._repository_spam_settings = repository_spam_settings

    def get(self, id):
        return self._repository_spam_settings.get(id=id)

    def create(self, obj_in: Any):
        if isinstance(obj_in, dict):
            return self._repository_spam_settings.create(obj_in=obj_in,
                                                         commit=True)

        return self._repository_spam_settings.get(name=obj_in)

    async def get_or_create(self, obj_in: Any):
        if isinstance(obj_in, dict):
            settings = self._repository_spam_settings.get(
                id=int(obj_in.get("id")))
            if settings is not None:
                return settings
            return self._repository_spam_settings.create(obj_in=obj_in,
                                                         commit=True)

        return self._repository_spam_settings.get(id=obj_in)

    async def update(self, id: int, obj_in: dict):
        return self._repository_spam_settings.update(
            db_obj=self._repository_spam_settings.get(id=id),
            obj_in=obj_in)
