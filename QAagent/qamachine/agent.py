from google.adk.agents.llm_agent import Agent

QA_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Question Answering Agent',
    instruction=""" 
    You are a helpful assisstant that answers questions about users prefrences.
    Here is some information about user:
    Name:
    {user_name}
    Preferences:
    {user_preferences} 
    """,
)
