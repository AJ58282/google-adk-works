from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool 
from google.adk.tools.tool_context import ToolContext 
from typing import Dict,Optional

def get_capital(country:str)->Dict[str,str]:
    """ 
    Returns capital of country
    Args:
        country:Name of the country
    Returns:
        Dictionary with the capital city result
    """

    print("Executing get_capital")
    country_capital={
        "united states":"D.C",
        "usa":"D.C",
        "canada":"ottawa",
        "france":"Paris",
        "india":"Delhi"
    }

def before_tool_callback(tool:BaseTool,args:Dict[str,Any],tool_context:ToolContext)->Optional[Dict]:
    """Simple callback that modifies the tool arguments or skips the tool call"""
    tool_name=tool.name
    print(f"before tool call:{tool_name}")


    if tool_name=="get_capital" and args.get("country","").lower()=="merica":
        print("converting merica to US")
        args["country"]="US"
        print(f"modified args{args}")
        return None

    if (tool_name=="get_capital" and args.get("country","").lower()=="restricted"):
        print("block restricted country")

    print("normal tool call")
    return None

def after_tool_callback(tool:BaseTool,args:Dict[str,Any],tool_context:ToolContext,tool_response:Dict)->Optional[Dict]:
    """ 
    Simple callback that modifies the tool response after execution.
    """
    tool_name=tool.name
    print(f"after tool callback:{tool_name}")
    print(f"original response:{tool_response}")
    original_result=tool_response.get("result","")
    print(f"original result:{original_result}")

    if tool_name=="get_capital" and "washington" in original_result.lower():
        print("USA detected")

        modified_response=copy.deepcopy(tool_response)
        modified_response["result"]=(f"{original_result}(capital of usa)")
        modified_response["noted_added_by_callback"]=True
        print(f"modified response {modified_response}")
        return modified_response
    
    print("no modifications") 
    return None


root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='An agent that determines tool callback capital cities',
    instruction='You are a geography assistant. Find the capital cities using get_capital',
    tools=[get_capital],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
