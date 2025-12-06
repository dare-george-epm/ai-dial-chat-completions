from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):
    """
    Client for interacting with Dial AI (sync and async).
    """

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._client = Dial(api_key=self._api_key, base_url=DIAL_ENDPOINT)
        self._async_client = AsyncDial(api_key=self._api_key, base_url=DIAL_ENDPOINT)

    def get_completion(self, messages: list[Message]) -> Message:
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=False,
            messages=[msg.to_dict() for msg in messages],
        )


        choices = response.choices
        if choices:
            message = choices[0].message
            if message:
                print(message.content)
                return Message(Role.AI, message.content)


        raise RuntimeError("No choices found in the AI response.")

    async def stream_completion(self, messages: list[Message]) -> Message:
        chunks = await self._async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages],
            stream=True,
        )

        contents = [] #To append streaming content
        async for chunk in chunks:
            choice = chunk.choices[0] if chunk.choices else None
            delta = choice.delta if choice else None

            if delta and delta.content:
                print(delta.content, end="")
                contents.append(delta.content)


        print()  
        return Message(Role.AI, "".join(contents))
