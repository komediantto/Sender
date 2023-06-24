
from app.repository.channel import ChannelRepository


class ChannelService:

    def __init__(self, repository_channel: ChannelRepository):
        self._repository_channel = repository_channel

    def get_or_create(self, obj_in: dict):
        if isinstance(obj_in, dict):
            channel = self._repository_channel.get(
                name=obj_in.get("name"))
            if channel is not None:
                return channel
            return self._repository_channel.create(obj_in=obj_in,
                                                   commit=True)

        return self._repository_channel.get(name=obj_in)
