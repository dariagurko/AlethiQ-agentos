import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNTBmY2M0My00NmM5LTRiMzUtOWMxNy0wYWI3Y2IyMDYwMzUiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjNkYjFjMTM3LTc0NDQtNDQ3Yi04MmFkLTc0ZjRjMTc0YTllMCJ9.hXI9NU6RfyFzQqa2WijhEW-_OnwA5syvNkq9ISAl3Ks" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="prompt_checker",
    description="Evaluates a GenAI prompt for ethical risks such as bias, misinformation, or harmful content."
)
async def prompt_checker(
    agent_context: GenAIContext,
    prompt_text: Annotated[str, "Prompt to evaluate"]
) -> str:
    flagged_keywords = ["kill", "suicide", "fake news", "gender roles", "extreme diet"]
    lower_text = prompt_text.strip().lower()

    for keyword in flagged_keywords:
        if keyword in lower_text:
            return f"⚠️ ETHICAL WARNING: The prompt contains potentially sensitive or harmful content ('{keyword}')"

    return f"✅ SAFE: No obvious ethical concerns found in prompt."


async def main():
    print(f"Prompt Checker running with token {AGENT_JWT}")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
