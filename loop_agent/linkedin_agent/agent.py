from google.adk.agents import SequentialAgent, LoopAgent
from .subagents.post_generator.agent import post_generator_agent
from .subagents.post_reviewer.agent import post_reviewer_agent
from .subagents.post_refiner.agent import post_refiner_agent

refinement_loop = LoopAgent(
    name="refinement_loop",
    max_iterations=5,
    sub_agents=[
        post_reviewer_agent,
        post_refiner_agent,
    ],
    description="Iteratively review and refine the LinkedIn post until it meets length requirements.",
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[
        post_generator_agent,
        refinement_loop,
    ],
    description="Generates and refines a LinkedIn post through an iterative process.",
)
