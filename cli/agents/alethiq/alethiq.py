import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext


AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzhlNGNlNS02ZDc0LTRmMjEtYmQ1OS01YWU2ZmFmYjEyNmYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjNkYjFjMTM3LTc0NDQtNDQ3Yi04MmFkLTc0ZjRjMTc0YTllMCJ9.M_UA1OPvvFGsEzAeyGDYZH7j3W50GUbzPOAE5QB3MzE" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="alethiq",
    description="Evaluates truthfulness and ethics of claims or AI-generated content."
)
async def alethiq_agent(agent_context: GenAIContext, text: str) -> dict:
  
    search_results = await agent_context.call_agent(
        "Web Search",        
        query=text
    )
    claim_eval = await agent_context.call_agent("claim_checker", claim_text=text)
    prompt_eval = await agent_context.call_agent("prompt_checker", prompt_text=text)

    return {
        "Web Search Results": search_results,
        "Claim Evaluation": claim_eval,
        "Prompt Evaluation": prompt_eval
        }

async def main():
    print(f"Alethiq agent running with token {AGENT_JWT}")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
