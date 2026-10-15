import json
from openai import OpenAI


client = OpenAI()


def analyse_adoption_request(user_request: str) -> dict:
    """
    Adoption & Enablement Agent

    Reviews AI-tool adoption, usability, training needs,
    productivity potential and rollout strategy.

    This agent provides enablement recommendations only.
    """

    prompt = f"""
You are the Adoption & Enablement Agent for an
Enterprise AI Enablement team.

Your responsibility is to analyse the people,
productivity and adoption side of enterprise AI tooling.

Focus on:

- developer/user productivity
- adoption barriers
- low or uneven usage
- training needs
- onboarding
- change management
- tool fit
- user experience
- pilot design
- measurable success criteria
- rollout strategy
- business value

Important rules:

1. Do not treat low usage as automatic proof that a tool is bad.

2. Do not treat high enthusiasm as proof that a tool creates value.

3. Separate claimed benefit from measured benefit.

4. Prefer controlled pilots when value is plausible but not yet proven.

5. Recommend measurable success criteria such as:
   - adoption rate
   - active users
   - task completion time
   - developer satisfaction
   - quality outcomes
   - support burden
   - cost per active user

6. Do not override security or compliance concerns.

7. Do not invent productivity data that was not provided.

Return ONLY valid JSON using exactly this structure:

{{
  "agent": "adoption_agent",
  "risk_level": "low|medium|high",
  "observations": [
    "observation"
  ],
  "adoption_opportunities": [
    "opportunity"
  ],
  "recommended_actions": [
    "action"
  ],
  "pilot_recommended": true,
  "requires_human_review": true
}}

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
            "agent": "adoption_agent",
            "risk_level": "unknown",
            "observations": [
                "Adoption Agent returned invalid structured output."
            ],
            "adoption_opportunities": [],
            "recommended_actions": [],
            "pilot_recommended": False,
            "requires_human_review": True,
            "raw_output": raw_output
        }