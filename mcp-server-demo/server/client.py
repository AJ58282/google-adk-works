from langchain_groq import ChatGroq
import asyncio

from mcp_use import MCPAgent,MCPClient
import os
from dotenv import load_dotenv


async def run_memory_chat():
    """ Run a chat using MCP's built in memory """
    load_dotenv()

    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    config_file="server/weather.json"

    print("Start")

    #mcpclient reading the data of config_file 
    client=MCPClient.from_config_file(config_file)
    llm=ChatGroq(model="llama-3.1-8b-instant")

    #creating an agent with memory enabled
    agent=MCPAgent(llm=llm,client=client,max_steps=15,memory_enabled=True)

    print("exit or quit to end convo")
    print("clear to clear the history")


    try:
        while True:
            user_input=input()

            if user_input.lower() in ['exit','quit']:
                print("breaking")
                break

            if user_input.lower()=='clear':
                agent.clear_conversation_history()
                print("convo history cleared")
                continue

            print("Assisstant:")
            try:
                response=await agent.run(user_input)
                print(response)
            
            except Exception as e:
                print(f"Error:{e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__=="__main__":
    asyncio.run(run_memory_chat())