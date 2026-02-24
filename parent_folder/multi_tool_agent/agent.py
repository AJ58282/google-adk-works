from google.adk.agents.llm_agent import Agent
import datetime
from zoneinfo import ZoneInfo

def get_weather(city:str)->dict:
    if city.lower()=='new york':
        return{
            'status':'success',
            'report':'weather is sunny'
        }
    else :
        return {
            'status':'error',
            'error_message':f'weather report for {city} not found'
    }

def get_time(city:str)->dict:
    if city.lower()=='new york':
        tz_id='America/New_York'
    else:
        return {
            'status':'error',
            'error_message':f'timezone for {city} not found'
        }
    tz=ZoneInfo(tz_id)
    now=datetime.datetime.now(tz)
    report=f'The time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S")}'
    return {
        'status':'success',
        'report': report
    }
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agent that can get weather and time information for a city',
    instruction='You are a helpful assistant that can get weather and time information for a city',
    tools=[get_weather,get_time]
)
