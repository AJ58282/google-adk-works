from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner 
from linkedin_agent.agent import root_agent
import asyncio
import uuid
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

async def main():
    USER_ID='adith'
    APP_NAME='agent'
    SESSION_ID=str(uuid.uuid4())

    session_service=InMemorySessionService()

    s_session=await session_service.create_session(app_name=APP_NAME,user_id=USER_ID,session_id=SESSION_ID)

    runner=Runner(app_name=APP_NAME,agent=root_agent,session_service=session_service)

    user_input=input()
    message=types.Content(role="user",parts=[types.Part(text=user_input)])

    async for event in runner.run_async(new_message=message,user_id=USER_ID,session_id=SESSION_ID):
        #there will be some output as None , so ignore them
        if not event.content and not event.content.parts:
            continue
        for part in event.content.parts:
            if hasattr(part,"text") and part.text:
                print(part.text)
            

if __name__=="__main__":
    asyncio.run(main())



