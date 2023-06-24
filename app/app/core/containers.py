from dependency_injector import containers, providers
from app.core.config import Settings
from app.db.session import SyncSession

from app.models.application import AccountTelethon, Channel, SpamSettings

from app.repository.account_telethon import AccountRepository
from app.repository.channel import ChannelRepository
from app.repository.spamsettings import SpamSettingsRepository

from app.services.account_telethon import AccountService
from app.services.channel import ChannelService
from app.services.spamsettings import SpamSettingsService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(
        SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_account_telethon = providers.Singleton(
        AccountRepository, model=AccountTelethon, session=db)
    repository_channel = providers.Singleton(
        ChannelRepository, model=Channel, session=db)
    repository_spam_settings = providers.Singleton(
        SpamSettingsRepository, model=SpamSettings, session=db)

    account_telethon_service = providers.Singleton(
        AccountService,
        repository_account_telethon=repository_account_telethon,
        repository_channel=repository_channel
    )
    channel_service = providers.Singleton(
        ChannelService,
        repository_channel=repository_channel
    )
    spam_settings_service = providers.Singleton(
        SpamSettingsService,
        repository_spam_settings=repository_spam_settings
    )
