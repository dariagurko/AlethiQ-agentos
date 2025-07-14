import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTFhYzA2Mi05M2VkLTQyOWUtOWNkOC02YjRmNGUzY2E0MDYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjNkYjFjMTM3LTc0NDQtNDQ3Yi04MmFkLTc0ZjRjMTc0YTllMCJ9.qd-N5xUBe8o5C4mn441NhdOKXM48i0ipKwePFZ16g2o" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="claim_checker",
    description="Evaluates whether a given claim is true, false, or misleading."
)
async def claim_checker(
    agent_context: GenAIContext,
    claim_text: Annotated[str, "Claim to verify"]
) -> str:
    prompt = (
        f"Evaluate the factual accuracy of the following claim: '{claim_text}'\n\n"
        "Respond in the format:\n"
        "Label: [True/False/Misleading/Unverifiable]\n"
        "Explanation: [One-sentence explanation why]"
    )
    response = await agent_context.llm.chat.completions.create(
            messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def main():
    print(f"Claim Checker running with token {AGENT_JWT}")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
