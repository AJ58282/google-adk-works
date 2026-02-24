from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from linkedin_agent.agent import root_agent
import asyncio
import uuid
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

db_url="sqlite+aiosqlite:///./my_agent_session.db"
session_service=DatabaseSessionService(db_url=db_url)

async def main():
    APP_NAME='adith'
    USER_ID='ad'
    SESSION_ID=str(uuid.uuid4())

    session=await session_service.create_session(user_id=USER_ID,session_id=SESSION_ID,app_name=APP_NAME)

    runner=Runner(agent=root_agent,app_name=APP_NAME,session_service=session_service)
    user_input=input()

    message=types.Content(role="user",parts=[types.Part(text=user_input)])

    async for event in runner.run_async(new_message=message,user_id=USER_ID,session_id=SESSION_ID):
        if not event.content or not event.content.parts:
            continue
        for part in event.content.parts:
            if hasattr(part,"text") and part.text:
                print(part.text)

if __name__=="__main__":
    asyncio.run(main())