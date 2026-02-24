from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext 
from datetime import datetime
from typing import Optional

def before_agent_callback(callback_context:CallbackContext)->Optional[types.Content]:
    """ 
    Simple Callback that logs when the agent starts processing requests.
    Args: 
        callback_context: contains state and context information
    Returns: 
        None to continue with normal agent processing
    """
    #session state
    state=callback_context.state

    timestamp=datetime.now()

    if "agent_name" not in state:
        state["agent_name"]="SimpleChatBot"
    
    if "request_counter" not in state:
        state["request_counter"]=1
    else:
        state["request_counter"]+=1


    state["request_start_time"]=timestamp.isoformat()

    #logging 
    print(f"Request count: {state["request_counter"]}")
    print(f"Timestamp: {timestamp.strftime("%Y-%m-%d %H-%M-%S")}")
    print(f"Before callback Agent processing request {state["request_counter"]}")
    return None

def after_agent_callback(callback_context:CallbackContext)->Optional[types.Content]:
    """ 
    Simple Callback that logs when the agent starts processing requests.
    Args: 
        callback_context: contains state and context information
    Returns: 
        None to continue with normal agent processing
    """

    state=callback_context.state
    timestamp=datetime.now()
    duration=None

    if "request_start_time" in state:
        start_time = datetime.fromisoformat(state["request_start_time"])
        duration = (timestamp - start_time).total_seconds()

    
    #logging the completion
    print("Execution done")
    print("Request:{state.get('request_counter','unknown)}")
    if duration is not None:
        print(f"duration :{duration:.2f} seconds")
    
    return None


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""You are a friendly agent.Answer user questions to the best of your knowledge""",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
