import uuid
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv
from qamachine.agent import QA_agent
from google.genai import types

load_dotenv()

async def main():

    session_service = InMemorySessionService()

    initial_state = {
        "user_name": "Adith Jose",
        "user_preferences": """
        I like to play BasketBall, Football.
        I like Indian cuisine.
        My favourite show is Friends.
        """
    }

    APP_NAME = "AJ"
    USER_ID = "A_J"
    SESSION_ID = str(uuid.uuid4())

    # ✅ Properly awaited session creation
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print("created new session")
    print(f"SESSION_ID: {SESSION_ID}")
    
    runner = Runner(
        agent=QA_agent,
        session_service=session_service,
        app_name=APP_NAME,
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text="What is Adith favourite sport?")]
    )
    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"Final response: {event.content.parts[0].text}")
    except Exception as e:
        print(f"Resource exhausted {e}")
    print("Session event")

    # ✅ Properly awaited get_session
    s_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("Final state:")
    for key, value in s_session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
