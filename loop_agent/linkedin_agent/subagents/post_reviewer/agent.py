from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .tools import count_char, exit_loop

post_reviewer_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="post_reviewer_agent",
    description="Checks LinkedIn post length and provides feedback.",
    instruction="""
    First, call the tool: count_char
    Use current_post as input.

    If the result status is "fail":
    - Explain what needs improvement.
    - Do not call any other tool.

    If the result status is "pass":
    - Say the post meets the length requirement.
    - Then call exit_loop.
    - Do not output anything after calling exit_loop.

    Return only feedback text.
    """,
    tools=[count_char, exit_loop],
    output_key="review_feedback",
)

