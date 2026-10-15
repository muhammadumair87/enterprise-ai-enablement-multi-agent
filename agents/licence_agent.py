import json
from openai import OpenAI


client = OpenAI()


def analyse_licence_request(user_request: str) -> dict:
    """
    Licence Agent

    Reviews licence utilisation, inactivity,
    entitlement and reassignment considerations.

    This agent provides recommendations only.
    It does not remove or reassign licences.
    """

    prompt = f"""
You are the Licence Governance Agent for an
Enterprise AI Enablement team.

Your responsibility is to analyse licence-related
aspects of an AI tooling request.

Focus on:

- inactive users
- licence utilisation
- licence assignment
- licence reassignment
- entitlement
- duplicate licences
- renewal decisions
- potential licence savings
- business justification

Important governance rules:

1. Never automatically remove a licence.

2. Inactivity is a review trigger,
   not proof that a licence is unnecessary.

3. Before recommending licence reclamation,
   consider:
   - leave
   - project timing
   - role changes
   - upcoming workloads
   - reporting accuracy
   - automation activity
   - business requirements

4. Clearly distinguish observations
   from recommendations.

5. Do not invent facts that are not present
   in the request.

Return ONLY valid JSON using this structure:

{{
  "agent": "licence_agent",
  "risk_level": "low|medium|high",
  "observations": [
    "observation"
  ],
  "recommended_actions": [
    "action"
  ],
  "potential_savings_review": true,
  "requires_human_review": true
}}

Request:

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
            "agent": "licence_agent",
            "risk_level": "unknown",
            "observations": [
                "Invalid structured output returned."
            ],
            "recommended_actions": [],
            "potential_savings_review": False,
            "requires_human_review": True,
            "raw_output": raw_output
        }