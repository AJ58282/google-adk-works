from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm

post_refiner_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="post_refiner_agent",
    description="Improves the LinkedIn post using reviewer feedback.",
    instruction="""
    You are refining a LinkedIn post.

    Available state:
    - current_post
    - review_feedback

    Use review_feedback to improve current_post.

    Requirements:
    - Improve clarity and structure
    - Strengthen hook
    - Improve flow
    - Keep professional tone
    - Keep between 1000-2000 characters
    - Keep hashtags if relevant
    - Do not add meta commentary

    Return only the updated LinkedIn post.
    """,
    output_key="current_post",
)
