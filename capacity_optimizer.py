import csv
from pathlib import Path


DATA_FILE = Path(
    "data/department_usage.csv"
)

SAFETY_BUFFER_PERCENT = 20


def load_department_usage():
    """
    Load synthetic departmental AI usage data.
    """

    departments = []

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            departments.append(
                {
                    "department":
                        row["department"],

                    "current_tokens":
                        int(row["current_tokens"]),

                    "token_limit":
                        int(row["token_limit"]),

                    "days_elapsed":
                        int(row["days_elapsed"]),

                    "days_in_month":
                        int(row["days_in_month"]),

                    "monthly_budget_eur":
                        float(
                            row["monthly_budget_eur"]
                        )
                }
            )

    return departments


def calculate_forecast(department):
    """
    Simple transparent linear month-end forecast.

    Example:
    3,000 tokens used in 20 days
    → 150 tokens/day
    → 4,500 tokens forecast for 30 days
    """

    days_elapsed = department[
        "days_elapsed"
    ]

    if days_elapsed <= 0:
        return 0

    daily_rate = (
        department["current_tokens"]
        / days_elapsed
    )

    forecast_tokens = (
        daily_rate
        * department["days_in_month"]
    )

    return round(
        forecast_tokens
    )


def analyse_capacity(departments):
    """
    Calculate forecast usage and determine
    possible donors and receivers.
    """

    analysed = []

    for department in departments:

        forecast_tokens = (
            calculate_forecast(
                department
            )
        )

        token_limit = department[
            "token_limit"
        ]

        forecast_usage_percent = (
            forecast_tokens
            / token_limit
            * 100
        )

        safety_buffer_tokens = round(
            token_limit
            * SAFETY_BUFFER_PERCENT
            / 100
        )

        projected_shortfall = max(
            0,
            forecast_tokens
            - token_limit
        )

        safe_transferable_capacity = max(
            0,
            token_limit
            - forecast_tokens
            - safety_buffer_tokens
        )

        if projected_shortfall > 0:

            status = "receiver_candidate"

        elif safe_transferable_capacity > 0:

            status = "donor_candidate"

        else:

            status = "balanced"

        analysed.append(
            {
                **department,

                "forecast_tokens":
                    forecast_tokens,

                "forecast_usage_percent":
                    round(
                        forecast_usage_percent,
                        1
                    ),

                "safety_buffer_tokens":
                    safety_buffer_tokens,

                "projected_shortfall":
                    projected_shortfall,

                "safe_transferable_capacity":
                    safe_transferable_capacity,

                "capacity_status":
                    status
            }
        )

    return analysed


def calculate_reallocations(
    analysed_departments
):
    """
    Produce recommended temporary reallocations.

    This function does NOT execute any change.
    It only calculates recommendations.
    """

    donors = [
        department.copy()
        for department
        in analysed_departments
        if department[
            "capacity_status"
        ] == "donor_candidate"
    ]

    receivers = [
        department.copy()
        for department
        in analysed_departments
        if department[
            "capacity_status"
        ] == "receiver_candidate"
    ]

    donors.sort(
        key=lambda item:
        item[
            "safe_transferable_capacity"
        ],
        reverse=True
    )

    receivers.sort(
        key=lambda item:
        item[
            "projected_shortfall"
        ],
        reverse=True
    )

    recommendations = []

    for receiver in receivers:

        remaining_shortfall = receiver[
            "projected_shortfall"
        ]

        for donor in donors:

            available = donor[
                "safe_transferable_capacity"
            ]

            if (
                remaining_shortfall <= 0
                or available <= 0
            ):
                continue

            transfer_amount = min(
                remaining_shortfall,
                available
            )

            recommendations.append(
                {
                    "from_department":
                        donor["department"],

                    "to_department":
                        receiver["department"],

                    "recommended_tokens":
                        transfer_amount,

                    "reason":
                        (
                            f"{receiver['department']} "
                            f"is forecast to exceed "
                            f"its allocation while "
                            f"{donor['department']} "
                            f"has forecast unused "
                            f"capacity after maintaining "
                            f"a {SAFETY_BUFFER_PERCENT}% "
                            f"safety buffer."
                        ),

                    "human_approval_required":
                        True
                }
            )

            donor[
                "safe_transferable_capacity"
            ] -= transfer_amount

            remaining_shortfall -= (
                transfer_amount
            )

    return recommendations


def run_capacity_optimizer():
    """
    Run complete deterministic capacity analysis.
    """

    departments = (
        load_department_usage()
    )

    analysed = (
        analyse_capacity(
            departments
        )
    )

    recommendations = (
        calculate_reallocations(
            analysed
        )
    )

    return {
        "safety_buffer_percent":
            SAFETY_BUFFER_PERCENT,

        "departments":
            analysed,

        "recommended_reallocations":
            recommendations,

        "automatic_changes_allowed":
            False,

        "human_approval_required":
            True
    }


if __name__ == "__main__":

    result = run_capacity_optimizer()

    print()
    print(
        "AI CAPACITY OPTIMISATION"
    )
    print("=" * 65)

    for department in result[
        "departments"
    ]:

        print()
        print(
            "Department:",
            department["department"]
        )

        print(
            "Current:",
            department["current_tokens"],
            "/",
            department["token_limit"]
        )

        print(
            "Forecast:",
            department[
                "forecast_tokens"
            ]
        )

        print(
            "Forecast usage:",
            f"{department['forecast_usage_percent']}%"
        )

        print(
            "Status:",
            department[
                "capacity_status"
            ]
        )

        print(
            "Safe transferable:",
            department[
                "safe_transferable_capacity"
            ]
        )

        print(
            "Projected shortfall:",
            department[
                "projected_shortfall"
            ]
        )

    print()
    print(
        "REALLOCATION RECOMMENDATIONS"
    )
    print("=" * 65)

    if not result[
        "recommended_reallocations"
    ]:

        print(
            "No capacity reallocation required."
        )

    for recommendation in result[
        "recommended_reallocations"
    ]:

        print()

        print(
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
            recommendation["reason"]
        )

        print(
            "Human approval required:",
            recommendation[
                "human_approval_required"
            ]
        )