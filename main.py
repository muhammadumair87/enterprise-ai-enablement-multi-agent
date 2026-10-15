import json
import os
from datetime import datetime

from agents.coordinator import route_request
from agents.licence_agent import analyse_licence_request
from agents.finops_agent import analyse_finops_request
from agents.security_agent import analyse_security_request
from agents.adoption_agent import analyse_adoption_request
from agents.report_agent import generate_governance_report
from capacity_optimizer import run_capacity_optimizer


# ==================================================
# 1. START
# ==================================================

print()
print("Enterprise AI Enablement Multi-Agent System")
print("=" * 60)

request = input(
    "\nEnter an AI Enablement request:\n> "
)


# ==================================================
# 2. COORDINATOR
# ==================================================

coordinator_result = route_request(
    request
)

print()
print("COORDINATOR DECISION")
print("-" * 60)

print(
    "Request summary:",
    coordinator_result.get(
        "request_summary"
    )
)

print(
    "Selected agents:",
    ", ".join(
        coordinator_result.get(
            "selected_agents",
            []
        )
    )
)

print(
    "Reasoning:",
    coordinator_result.get(
        "reasoning_summary"
    )
)

print(
    "Human review required:",
    coordinator_result.get(
        "requires_human_review"
    )
)


# ==================================================
# 3. PREPARE SPECIALIST EXECUTION
# ==================================================

selected_agents = coordinator_result.get(
    "selected_agents",
    []
)

specialist_results = []

capacity_analysis = None


# ==================================================
# 4. LICENCE AGENT
# ==================================================

if "licence_agent" in selected_agents:

    print()
    print("Running Licence Agent...")

    licence_result = analyse_licence_request(
        request
    )

    specialist_results.append(
        licence_result
    )


# ==================================================
# 5. FINOPS + CAPACITY OPTIMIZER
# ==================================================

if "finops_agent" in selected_agents:

    print()
    print("Running Capacity Optimizer...")

    capacity_analysis = (
        run_capacity_optimizer()
    )

    print()
    print("CAPACITY OPTIMIZER RESULT")
    print("-" * 60)

    for department in capacity_analysis.get(
        "departments",
        []
    ):

        print(
            department["department"],
            "| current:",
            department["current_tokens"],
            "/",
            department["token_limit"],
            "| forecast:",
            department["forecast_tokens"],
            "| usage:",
            f"{department['forecast_usage_percent']}%",
            "| status:",
            department["capacity_status"]
        )

    recommendations = (
        capacity_analysis.get(
            "recommended_reallocations",
            []
        )
    )

    if recommendations:

        print()
        print(
            "Recommended reallocations:"
        )

        for recommendation in recommendations:

            print(
                "-",
                recommendation[
                    "from_department"
                ],
                "→",
                recommendation[
                    "to_department"
                ],
                ":",
                recommendation[
                    "recommended_tokens"
                ],
                "tokens"
            )

            print(
                " ",
                recommendation[
                    "reason"
                ]
            )

    else:

        print()
        print(
            "No reallocation recommendation generated."
        )

    print()
    print("Running FinOps Agent...")

    finops_result = (
        analyse_finops_request(
            request,
            capacity_analysis
        )
    )

    specialist_results.append(
        finops_result
    )


# ==================================================
# 6. SECURITY AGENT
# ==================================================

if "security_agent" in selected_agents:

    print()
    print("Running Security Agent...")

    security_result = (
        analyse_security_request(
            request
        )
    )

    specialist_results.append(
        security_result
    )


# ==================================================
# 7. ADOPTION AGENT
# ==================================================

if "adoption_agent" in selected_agents:

    print()
    print("Running Adoption Agent...")

    adoption_result = (
        analyse_adoption_request(
            request
        )
    )

    specialist_results.append(
        adoption_result
    )


# ==================================================
# 8. DISPLAY SPECIALIST RESULTS
# ==================================================

print()
print("SPECIALIST AGENT RESULTS")
print("=" * 60)

if not specialist_results:

    print(
        "No implemented specialist agent was selected."
    )


for result in specialist_results:

    print()

    print(
        "Agent:",
        result.get(
            "agent"
        )
    )

    print(
        "Risk level:",
        result.get(
            "risk_level"
        )
    )

    print("Observations:")

    for observation in result.get(
        "observations",
        []
    ):

        print(
            "-",
            observation
        )


    if result.get(
        "capacity_findings"
    ):

        print(
            "Capacity findings:"
        )

        for finding in result.get(
            "capacity_findings",
            []
        ):

            print(
                "-",
                finding
            )


    if result.get(
        "recommended_actions"
    ):

        print(
            "Recommended actions:"
        )

        for action in result.get(
            "recommended_actions",
            []
        ):

            print(
                "-",
                action
            )


    if result.get(
        "security_risks"
    ):

        print(
            "Security risks:"
        )

        for risk in result.get(
            "security_risks",
            []
        ):

            print(
                "-",
                risk
            )


    if result.get(
        "recommended_controls"
    ):

        print(
            "Recommended controls:"
        )

        for control in result.get(
            "recommended_controls",
            []
        ):

            print(
                "-",
                control
            )


    if result.get(
        "adoption_opportunities"
    ):

        print(
            "Adoption opportunities:"
        )

        for opportunity in result.get(
            "adoption_opportunities",
            []
        ):

            print(
                "-",
                opportunity
            )


    if (
        "supports_reallocation"
        in result
    ):

        print(
            "Supports reallocation:",
            result.get(
                "supports_reallocation"
            )
        )


    print(
        "Human review required:",
        result.get(
            "requires_human_review"
        )
    )


# ==================================================
# 9. GOVERNANCE DECISION AGENT
# ==================================================

print()
print(
    "Running Governance Decision Agent..."
)

governance_report = (
    generate_governance_report(
        request,
        coordinator_result,
        specialist_results,
        capacity_analysis
    )
)


# ==================================================
# 10. FINAL GOVERNANCE DECISION
# ==================================================

print()
print(
    "FINAL GOVERNANCE DECISION"
)
print("=" * 60)

print(
    "Decision:",
    governance_report.get(
        "final_decision"
    )
)

print(
    "Overall risk:",
    governance_report.get(
        "overall_risk"
    )
)

print()
print(
    "Executive summary:"
)

print(
    governance_report.get(
        "executive_summary"
    )
)


print()
print(
    "Key findings:"
)

for finding in governance_report.get(
    "key_findings",
    []
):

    print(
        "-",
        finding
    )


capacity_summary = (
    governance_report.get(
        "capacity_reallocation_summary",
        []
    )
)

if capacity_summary:

    print()
    print(
        "Capacity reallocation summary:"
    )

    for item in capacity_summary:

        print(
            "-",
            item
        )


print()
print(
    "Conflicts / trade-offs:"
)

for tradeoff in governance_report.get(
    "conflicts_or_tradeoffs",
    []
):

    print(
        "-",
        tradeoff
    )


print()
print(
    "Decision conditions:"
)

for condition in governance_report.get(
    "decision_conditions",
    []
):

    print(
        "-",
        condition
    )


print()
print(
    "Recommended actions:"
)

for action in governance_report.get(
    "recommended_actions",
    []
):

    print(
        "-",
        action
    )


print()
print(
    "Human approval required:",
    governance_report.get(
        "requires_human_approval"
    )
)


# ==================================================
# 11. JSON AUDIT TRAIL
# ==================================================

os.makedirs(
    "reports",
    exist_ok=True
)

timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

audit_record = {
    "timestamp":
        timestamp,

    "request":
        request,

    "coordinator_result":
        coordinator_result,

    "capacity_analysis":
        capacity_analysis,

    "specialist_results":
        specialist_results,

    "governance_report":
        governance_report
}

audit_filename = (
    "reports/"
    f"governance_decision_{timestamp}.json"
)

with open(
    audit_filename,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        audit_record,
        file,
        indent=2,
        ensure_ascii=False
    )


print()
print("AUDIT TRAIL")
print("=" * 60)

print(
    "Audit record saved:",
    audit_filename
)


# ==================================================
# 12. COMPLETE
# ==================================================

print()
print("=" * 60)

print(
    "Enterprise AI Enablement workflow complete."
)