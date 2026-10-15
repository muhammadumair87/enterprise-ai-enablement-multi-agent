import json
from typing import Optional
from openai import OpenAI


client = OpenAI()


def analyse_finops_request(
    user_request: str,
    capacity_analysis: Optional[dict] = None
) -> dict:
    """
    FinOps Agent

    Reviews AI usage, token consumption,
    budgets, forecasts and capacity.

    Deterministic forecast calculations may be
    supplied by the Python capacity optimizer.

    The agent interprets those calculations but
    must not invent or modify them.
    """

    context = {
        "user_request": user_request,
        "capacity_analysis": capacity_analysis
    }

    prompt = f"""
You are the AI FinOps Agent for an
Enterprise AI Enablement team.

Your responsibility is to analyse financial,
usage and capacity implications of enterprise
AI tooling.

Focus on:

- token consumption
- API usage
- AI spend
- departmental budgets
- usage limits
- capacity planning
- forecast utilisation
- underutilised capacity
- projected shortages
- temporary capacity reallocation
- cost optimisation

IMPORTANT ARCHITECTURE RULE:

If deterministic capacity analysis is supplied,
those numbers were calculated by a Python
governance engine.

Treat those numbers as the source of truth.

Do NOT:
- recalculate them
- change them
- invent different transfer amounts
- claim that a recommended transfer has already occurred

The Python engine may identify:

- donor departments
- receiver departments
- forecast usage
- safe transferable capacity
- projected shortfalls
- recommended temporary reallocations

Your role is to interpret whether the recommendation
is operationally reasonable.

Governance rules:

1. High utilisation does not automatically justify
   increasing spend.

2. Underutilisation does not automatically justify
   taking capacity away.

3. Before supporting reallocation, consider:
   - expected upcoming workload
   - business criticality
   - seasonality
   - automation activity
   - reporting accuracy
   - minimum reserve capacity
   - whether the vendor supports such allocation changes

4. Prefer optimisation of existing capacity before
   purchasing additional capacity when appropriate.

5. Reallocation recommendations require human approval.

6. Do not invent facts that are not present.

Return ONLY valid JSON:

{{
  "agent": "finops_agent",
  "risk_level": "low|medium|high",
  "observations": [
    "observation"
  ],
  "budget_status": "healthy|warning|critical|unknown",
  "capacity_findings": [
    "finding"
  ],
  "recommended_actions": [
    "action"
  ],
  "supports_reallocation": true,
  "capacity_review_required": true,
  "requires_human_review": true
}}

INPUT:

{json.dumps(context, indent=2)}
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
            "agent": "finops_agent",
            "risk_level": "unknown",
            "observations": [
                "FinOps Agent returned invalid structured output."
            ],
            "budget_status": "unknown",
            "capacity_findings": [],
            "recommended_actions": [],
            "supports_reallocation": False,
            "capacity_review_required": True,
            "requires_human_review": True,
            "raw_output": raw_output
        }