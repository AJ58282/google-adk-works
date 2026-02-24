from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

post_generator_agent = LlmAgent(
    name="post_generator",
    model="gemini-2.5-flash",
    description="Generates a LinkedIn post about Agentic AI.",
    instruction="""
    Write a professional LinkedIn post about Agentic AI.
    Requirements:
    - Strong opening hook (1-2 lines)
    - Clear explanation
    - Practical insights
    - Short paragraphs (1-3 lines)
    - Professional tone
    - 3-5 relevant hashtags at the end

    Return only the LinkedIn post text.
    """,
    output_key="current_post",
)
