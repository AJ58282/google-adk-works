from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from dotenv import load_dotenv
from google.genai import types
from google.adk.models.google_llm import _ResourceExhaustedError


def process_agent_response(event):
    if event.is_final_response():
        if event.content and event.content.parts:
            return event.content.parts[0].text
    return None

async def display_state(session_service,app_name,user_id,session_id,label="Current state"):
    session=await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"{label}")
    for k,v in session.state.items():
        print(f"{k}:{v}")

async def call_agent_async(runner,user_id,session_id,query):
    content=types.Content(role="user",parts=[types.Part(text=query)])
    print("Running Query")
    final_response_text=None

    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State before processing"
    )
    try:
        async for event in runner.run_async(user_id=user_id,new_message=content,session_id=session_id):
            response=process_agent_response(event)
            if response:
                final_response_text=response
                break
    except _ResourceExhaustedError:
        print(f"Quota exhausted!")
        return None
    except Exception as e:
        print(f"Error during call :{e}")
        return None

    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State after processing"
        )

    return final_response_text