from remote_mcp.prompt import NOTION_PROMPT
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


NOTION_PROMPT=os.getenv("NOTION_API_KEY")
if NOTION_PROMPT is None:
    raise ValueError("NOTION_API_KEY is not set.")

NOTION_MCP_HEADER=json.dumps({"Authorization":f"Bearer {NOTION_API_KEY}","Notion-Version":"2025"})


root_agent = Agent(
    model='',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=NOTION_PROMPT,
    tools=[
        MCPToolset()
    ]
)


