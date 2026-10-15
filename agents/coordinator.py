import json
from openai import OpenAI


client = OpenAI()


def route_request(user_request: str) -> dict:
    """
    Coordinator Agent

    Decides which specialist agents should analyse
    an AI Enablement request.
    """

    prompt = f"""
You are the Coordinator Agent for an Enterprise AI Enablement team.

Your job is to analyse the incoming request and decide which specialist
agents should be involved.

Available specialist agents:

1. licence_agent
   Handles:
   - AI tool licences
   - inactive users
   - licence assignment
   - entitlement
   - licence optimisation
   - renewal / removal review

2. finops_agent
   Handles:
   - AI usage
   - token consumption
   - cost
   - budgets
   - capacity
   - forecasting
   - high or low utilisation

3. security_agent
   Handles:
   - security
   - privacy
   - data protection
   - access control
   - sensitive data
   - governance risk
   - compliance concerns

4. adoption_agent
   Handles:
   - user adoption
   - training
   - enablement
   - low usage
   - tool fit
   - developer/user experience

The coordinator may select more than one agent.

Do not solve the request yourself.

Return ONLY valid JSON in exactly this structure:

{{
  "request_summary": "short summary",
  "selected_agents": [
    "licence_agent",
    "finops_agent"
  ],
  "reasoning_summary": "brief explanation of why these agents are needed",
  "requires_human_review": true
}}

Important:
- Use only agent names from the available list.
- Select only agents that are relevant.
- Enterprise AI governance decisions should normally require human review.

Incoming request:

{user_request}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    raw_output = response.output_text.strip()

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        return {
            "request_summary": user_request,
            "selected_agents": [],
            "reasoning_summary":
                "Coordinator returned invalid structured output.",
            "requires_human_review": True,
            "raw_output": raw_output
        }