from app.db.base_class import Base
from sqlalchemy import Column, Integer, String


class AccountTelethon(Base):
    '''Модель содержит сообщение, количество продукта, дату создания, id канала''' # noqa

    __tablename__ = 'accounttelethon'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=False)
    api_id = Column(Integer, nullable=False)
    api_hash = Column(String, nullable=False)
    session = Column(String, nullable=False)


class Channel(Base):
    """Модель содержит название канала."""

    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class SpamSettings(Base):

    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    delay = Column(Integer, default=5)
    dialog_limit = Column(Integer, default=20)
    template_message = Column(String, default='Welcome to the chat!')
