import json
from openai import OpenAI


client = OpenAI()


def analyse_security_request(user_request: str) -> dict:
    """
    Security & Governance Agent

    Analyses enterprise AI requests for security,
    privacy, identity and governance risks.

    This agent recommends controls but does not
    automatically block tools or users.
    """

    prompt = f"""
You are the Security & Governance Agent in an
Enterprise AI Enablement platform.

Analyse the following request from an enterprise
security and AI-governance perspective.

Evaluate:

- confidential or sensitive data exposure
- personal/customer data
- proprietary source code
- credentials, API keys and secrets
- identity and access management
- excessive permissions
- approved versus unapproved AI tools
- third-party AI services
- data retention
- data residency
- auditability
- compliance implications
- security guardrails

Governance rules:

1. Never invent a confirmed security incident.

2. Clearly distinguish between an observed fact
   and a potential security risk.

3. Never automatically disable a user or AI tool.

4. Never assume an internal company policy exists
   unless it appears in the request.

5. High-risk situations require human/security review.

6. Prefer controlled enablement with appropriate
   guardrails where risk can reasonably be mitigated.

7. If information is insufficient, recommend what
   should be validated rather than inventing facts.

Return ONLY valid JSON:

{{
    "agent": "security_agent",
    "risk_level": "low|medium|high",
    "observations": [
        "observation"
    ],
    "security_risks": [
        "risk"
    ],
    "recommended_controls": [
        "control"
    ],
    "requires_security_review": true,
    "requires_human_review": true
}}

REQUEST:

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
            "agent": "security_agent",
            "risk_level": "unknown",
            "observations": [
                "Security Agent returned invalid structured output."
            ],
            "security_risks": [],
            "recommended_controls": [],
            "requires_security_review": True,
            "requires_human_review": True,
            "raw_output": raw_output
        }