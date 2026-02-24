from google.adk.agents.llm_agent import Agent
import datetime


def get_current_time():
    time=datetime.now()
    return {
        "action":"get_current_time",
        "current_time":now.strftime("%Y-%m-%d %H:%M:%S")
    }
