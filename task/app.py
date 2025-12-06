import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start_chat(stream: bool = True) -> None:
    """
    Start an interactive chat session with the DialClient.
    """
    
    custom_client = DialClient(deployment_name="gpt-4o")  
    conversation = Conversation()

    print("Provide a system prompt, or press Enter to use the default:")
    prompt = input("> ").strip()

    if prompt:
        conversation.add_message(Message(Role.SYSTEM, prompt))
        print("✅ System prompt added to conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"⚠ Using default system prompt: '{DEFAULT_SYSTEM_PROMPT}'")

    print("\nChat is ready. Type your message or 'exit' to quit.\n")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("👋 Exiting chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_input))

        print("AI:")
        if stream:
            ai_message = await custom_client.stream_completion(conversation.get_messages())
        else:
            ai_message = custom_client.get_completion(conversation.get_messages())

        conversation.add_message(ai_message)

if __name__ == "__main__":
    asyncio.run(start_chat(stream=True))
