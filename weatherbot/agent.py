from google.adk.agents.llm_agent import Agent
from google.adk.session import InMemorySessionServiceSession
from google.adk.runner import Runner
from google.genai import types
from typing import Optional

import asyncio
import warnings
warnings.filterwarnings('ignore')

#SIMPLE tool 
def get_weather(city:str)->dict:
    print(f"tool:get_weather called for city:{city}")
    city_norm=city.lower().replace(' ','')

    db={
        'new york':{
            'status':'success',
            'report':'sunny'
        },
        'london':{
            'status':'success',
            'report':'cloudy'
        },
    }

    if city_norm in db:
        return db[city_norm]
    else:
        return {
            'status':'error',
            'error_message':f'sorry'
        }

#USING SUB AGENTS
def say_hello(name:Optional[str]=None):
    if name:
        greeting= f"Hello {name}"
    else:
        greeting= f"Hello there"
    return greeting


def say_goodbye()->str:
    return "Goodbye!"

AGENT_MODEL="gemini-2.5-flash"

greeting_agent=None
try:
    greeting_agent=Agent(
        name='greeting agent',
        model=AGENT_MODEL,
        description="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks."",
        instructions="Handles simple greetings and hellos using the 'say_hello' tool."
        tools=[say_hello]
    )
except Exception as e:
    print(f"check api key{greeting_agent.model}") 


farewell_agent=None
try:
    farewell_agent=Agent(
        name='farewell agent',
        model=AGENT_MODEL,
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                    "Do not perform any other actions.",
        tools=[say_goodbye]
    )
    print(f"Agent {farewell_agent.name} created using {farewell_agent.model}")
except Exception as e:
    print(f"Check API key {farewell_agent.model}.Error: {e}")

if greeting_agent and farewell_agent and get_weather in globals():
    root_agent_model=AGENT_MODEL
    weather_agent=Agent(
        model=root_agent_model
        name="weather_agentv2"
        description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
        instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                    "You have specialized sub-agents: "
                    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                    "If it's a weather request, handle it yourself using 'get_weather'. "
                    "For anything else, respond appropriately or state you cannot handle it.",
        tool=[get_weather],
        sub_agents=[greeting_agent,farewell_agent]
)

#creating session and its details for it to run asynchronously

session_service=InMemorySessionService()

APP_NAME="weather_app"
USER_ID="user_1"
SESSION_ID="session_1"


async def init_session():
    session= await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created:App={APP_NAME},User={USER_ID},Session={SESSION_ID}")
    return session

runner = Runner(
    agent=weather_agent,
    app_name=APP_NAME,
    session_service=session_service
)

async def call_agent_async(query:str,session_id,user_id,runner):
    content=types.Content(role='user',parts=[types.Part(text=query)])
    
    #default reponse when nothing as output
    final_reponse_text='No response'

    async for event in runner.run_async(session_id=SESSION_ID,user_id=USER_ID,new_message=content):
        if event.is_final_reponse():
            if event.content and event.content.parts:
                final_reponse_text=event.content.parts[0].text
            elif event.actions abd event.actions.escalate:
                final_reponse_text="Agent escalated"
            break

async def run_conversation():
    await init_session()

    await call_agent_async("What is weather in london",runner=runner,session_id=SESSION_ID,user_id=USER_ID)
    await call_agent_async("What is weather in delhi",runner=runner,session_id=SESSION_ID,user_id=USER_ID)
    await call_agent_async("What is weather in new york",runner=runner,session_id=SESSION_ID,user_id=USER_ID)
    
await run_conversation()