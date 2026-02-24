from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async
from dotenv import load_dotenv
import asyncio

load_dotenv()

#Using a database SQLlite

db_url="sqlite+aiosqlite:///./my_agent_db.db"
session_service=DatabaseSessionService(db_url=db_url)

#Initial state only when new session
initial_state={
    "user_name":"Adith",
    "reminders":[],
}

async def main():
    APP_NAME="memory_agent"
    USER_ID="trial"

    #checking for exisiting session
    exisiting_session=await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    #If exisiting sessions exists
    if exisiting_session and len(exisiting_session.sessions)>0:
        SESSION_ID=exisiting_session.sessions[0].id 
        print(f"Exisiting session:{SESSION_ID}")

    #If no exisiting session , create a new session
    else:
        new_session=await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID=new_session.id 
        print(f"Created new session:{SESSION_ID}")
    
    runner=Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service
    )


    print("Memory Agent Chat")
    while True:
        user_input=input("You:")

        if user_input.lower() in ["exit","quit"]:
            print("End convo")
            break

        await call_agent_async(runner,USER_ID,SESSION_ID,user_input)

if __name__=="__main__":
    asyncio.run(main())