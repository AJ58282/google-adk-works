from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest,LlmResponse
from google.genai import types 
from datetime import datetime
from typing import Optional
import copy
import uuid
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner 
import asyncio


def before_model_callback(callback_context:CallbackContext,llm_request:LlmRequest)->Optional[LlmResponse]:
    """ This callback runs before the model processes a request.
        It filters inappropriate content and logs request info.
        
        Args: 
            callback_context: contains state and context information
            llm_request: The llm request being sent.
        Returns:
            Optional Llm response to override model response.
        """
    state=callback_context.state
    agent_name=callback_context.agent_name

    # extracting the last user message
    last_user_message=""
    if llm_request.contents and len(llm_request.contents)>0:
        for content in reversed(llm_request.contents):
            if content.role=="user" and content.parts and len(content.parts)>0:
                if hasattr(content.parts[0],"text") and content.parts[0].text:
                    last_user_message=content.parts[0].text
                    break 
    print("model request started")
    print(f"agent name {agent_name}")
    if last_user_message:
        print(f"User message:{last_user_message[:100]}")
        state["last_user_message"]=last_user_message
    else:
        print("User message:<empty>")
    

    #checking for inappropriate content
    if last_user_message and "sucks" in last_user_message.lower():
        print("Blocked")

        return LlmResponse(content=types.Content(role="model",parts=[types.Part(text="please rephrase")]))
    #if bad word did not occur
    state["model_start_time"]=datetime.now().isoformat()
    print("Approved")

    #proceed normally
    return None



def after_model_callback(callback_context:CallbackContext,llm_response:LlmResponse)->Optional[LlmResponse]:
    """ 
    Simple callback that replaces negative words with positive replacements.
    Args:
        callback_content: contains state and context information
        llm_response:The llm response received
    Returns:
        Optional LlmResponse:LlmResponse to override model response
    """

    print("Processing response")

    # if llm response is empty or has no text
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None 
    #extract text from response
    response_text=""
    for part in llm_response.content.parts:
        if hasattr(part,"text") and part.text:
            response_text+=part.text
    
    if not response_text:
        return None

    replacements={
        "problem":"challenge",
        "difficult":"complex",
    }

    modified_text=response_text
    modified=False

    for original,replacement in replacements.items():
        if original in modified_text.lower():
            modified_text=modified_text.replace(original,replacement)
            modified_text=modified_text.replace(original.capitalize(),replacement.capitalize())
            modified=True

    if modified:
        print("Modified response")
        modified_parts=[copy.deepcopy(part) for part in llm_response.content.parts]
        for i,part in enumerate(modified_parts):
            if hasattr(part,"text") and part.text:
                modified_parts[i].text=modified_text

        return LlmResponse(content=types.Content(role="model",parts=modified_parts))
    
    return None



root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent demonstrating callbacks for filtering',
    instruction=""" You are a helpful assistant, answer all questions nicely and accurately""",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback
)


async def main():
    APP_NAME="app"
    SESSION_ID=str(uuid.uuid4())
    USER_ID="local"


    session_service=InMemorySessionService()

    session=await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={}
    )


    runner=Runner(
        agent=root_agent,
        session_service=session_service,
        app_name=APP_NAME
    )

    while True:
        user_input=input()

        if user_input.lower() in ["exit","quit"]:
            break
        
        message=types.Content(role="user",parts=[types.Part(text=user_input)])

        async for event in runner.run_async(user_id=USER_ID,session_id=SESSION_ID,new_message=message):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print("agent:",event.content.parts[0].text)

if __name__=="__main__":
    asyncio.run(main())
