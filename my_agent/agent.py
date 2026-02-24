from google.adk.agents.llm_agent import Agent
from datetime import datetime
from zoneinfo import ZoneInfo


def get_time(city:str)->dict:
    return {"city":city, "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=''' If the user asks you to provide time in a city, use the get_time tool to get the time in the city. ''',
    tools=[get_time]
)
