# Enterprise AI Enablement Multi-Agent System

A privacy-safe enterprise AI enablement prototype that combines multi-agent orchestration, deterministic capacity optimisation, AI FinOps, licence governance, security assessment, adoption analysis, human approval gates and auditable governance decisions.

> **Portfolio Project 2 — Enterprise AI Enablement & Decision Orchestration**

---

## Overview

Enterprise AI adoption creates operational challenges that extend beyond deploying individual tools.

As organisations introduce platforms such as GitHub Copilot, ChatGPT Enterprise, Cursor and other AI services, AI Enablement and R&D Operations teams must continuously balance:

- productivity
- licence utilisation
- AI consumption
- cost
- security
- privacy
- adoption
- capacity
- business demand
- governance

Many enterprise AI decisions therefore require input from several different operational perspectives.

This prototype explores how a coordinator and specialist AI agents can support those decisions while keeping deterministic calculations, high-impact actions and approval authority outside the LLM.

---

## Core Design Principle

The architecture deliberately separates:

```text
Deterministic calculation
        +
AI-assisted interpretation
        +
Human approval
```

A key principle is:

> **Use deterministic software for calculations and LLMs for interpretation, coordination and decision support.**

For example, the Capacity Optimizer calculates forecast utilisation, safety buffers and transferable capacity using Python.

The AI agents may interpret those figures, but they are instructed not to invent or change the calculated values.

---

## System Architecture

```text
                     ENTERPRISE REQUEST
                            │
                            ▼
                    ┌───────────────┐
                    │  Coordinator  │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
 ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
 │ Licence Agent  │ │  FinOps Agent  │ │ Security Agent │
 └────────────────┘ └───────┬────────┘ └────────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Capacity Optimizer  │
                  │ Deterministic Python│
                  └─────────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
 ┌────────────────┐                  ┌────────────────┐
 │ Adoption Agent │                  │ Specialist     │
 │                │                  │ Findings       │
 └────────────────┘                  └────────────────┘
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Governance / Report │
                  │       Agent         │
                  └──────────┬──────────┘
                             │
                             ▼
                    Final Recommendation
                             │
                             ▼
                    Human Approval Gate
                             │
                             ▼
                       JSON Audit Trail
```

---

## Agent Roles

### Coordinator Agent

The Coordinator is the entry point for a business request.

It analyses the request and decides which specialist agents should participate.

Example:

```text
Request:
A development team wants to use an unreviewed external
AI coding assistant with customer data.

Coordinator:

Selected agents:
- security_agent
- adoption_agent

Human review required:
True
```

The Coordinator avoids executing every specialist for every request.

This demonstrates dynamic routing rather than a fixed sequential workflow.

---

### Licence Agent

The Licence Agent evaluates questions concerning:

- inactive users
- entitlement utilisation
- unused licences
- reassignment opportunities
- licence review
- renewal decisions

An important governance rule is:

> Inactivity is a review trigger, not proof that a licence should automatically be removed.

Possible context may include:

- leave
- project timing
- role changes
- automation
- future workload
- shared responsibilities

Human review remains required before entitlement changes.

---

### FinOps Agent

The FinOps Agent focuses on:

- AI consumption
- token usage
- departmental budgets
- usage limits
- projected demand
- capacity pressure
- cost optimisation
- allocation efficiency

Where deterministic capacity analysis is available, the FinOps Agent treats those calculations as the numerical source of truth.

It is explicitly instructed not to invent transfer amounts or claim that a recommendation has already been implemented.

---

### Security Agent

The Security Agent evaluates enterprise AI requests for risks involving:

- confidential information
- personal data
- proprietary source code
- secrets and credentials
- vendor security review
- data retention
- model training
- data residency
- access controls
- auditability
- compliance

Example high-risk scenario:

```text
Customer data
+
Proprietary source code
+
Unreviewed external AI service
=
Security review required
```

The agent does not automatically approve or block production systems.

It provides structured risks and recommended controls for human decision makers.

---

### Adoption Agent

The Adoption Agent evaluates the user and business-value side of AI adoption.

It focuses on:

- productivity opportunities
- adoption barriers
- onboarding
- training
- user experience
- pilot design
- success metrics
- rollout strategy
- change management

It deliberately separates:

```text
Claimed productivity benefit
            ≠
Measured productivity benefit
```

Potential metrics include:

- active-user adoption
- task completion time
- developer satisfaction
- quality outcomes
- support burden
- cost per active user

---

### Governance Decision / Report Agent

The Report Agent reconciles:

- the original request
- Coordinator routing
- specialist findings
- deterministic capacity calculations

It produces one management-oriented recommendation.

Possible decisions include:

```text
APPROVE
APPROVE_WITH_CONTROLS
CONDITIONAL_PILOT
HOLD_FOR_REVIEW
DO_NOT_APPROVE
```

The report also identifies:

- overall risk
- key findings
- capacity implications
- conflicts and trade-offs
- decision conditions
- recommended actions
- whether human approval is required

---

## Deterministic Capacity Optimizer

Capacity optimisation is intentionally implemented in Python rather than delegated to an LLM.

The optimizer reads synthetic departmental usage data and calculates:

- current usage
- projected month-end usage
- forecast utilisation
- projected shortfalls
- safety buffers
- safe transferable capacity
- donor departments
- receiver departments
- recommended temporary reallocations

Example:

```text
IT

Current:
9,000 / 10,000 tokens

Forecast:
13,500 tokens

Projected shortfall:
3,500 tokens
```

Another department may have spare capacity:

```text
Finance

Forecast:
1,350 / 10,000 tokens

Calculated safe transferable capacity:
6,650 tokens
```

The deterministic recommendation can therefore become:

```text
Finance → IT
3,500 tokens
```

The system does **not** execute this transfer.

It sends the calculated recommendation to the FinOps and Governance layers.

---

## Safety Buffer

The capacity optimizer preserves configurable reserve capacity before identifying a department as a potential donor.

Example:

```text
Department limit:
10,000

Forecast consumption:
4,500

Safety buffer:
2,000

Maximum safe transferable capacity:
3,500
```

This prevents the system from treating all apparently unused capacity as immediately available.

---

## Example Capacity Governance Workflow

```text
Usage telemetry
      │
      ▼
Forecast month-end consumption
      │
      ▼
Identify capacity pressure
      │
      ▼
Identify underutilised allocation
      │
      ▼
Apply safety buffer
      │
      ▼
Calculate safe transfer
      │
      ▼
FinOps interpretation
      │
      ▼
Governance decision
      │
      ▼
Human approval
      │
      ▼
Monitoring / rollback
```

This allows the system to consider optimisation of existing capacity before recommending additional spend.

---

## Example Scenario 1 — Capacity Reallocation

Business request:

```text
IT has already consumed 90% of its monthly AI token
allocation after 20 days while other departments appear
underutilised.

Can we avoid additional spend by reallocating unused
capacity to IT?
```

The deterministic optimizer identifies:

```text
IT projected requirement:
13,500 tokens

IT projected shortfall:
3,500 tokens

Finance safe transferable capacity:
6,650 tokens
```

Recommendation:

```text
Temporary transfer:
Finance → IT

Amount:
3,500 tokens
```

The Governance Agent may then return:

```text
Decision:
CONDITIONAL_PILOT

Overall risk:
medium

Human approval:
required
```

Conditions may include:

- validate Finance's remaining workload
- confirm vendor/platform support
- keep the transfer temporary
- document ownership
- define rollback conditions
- monitor usage
- avoid additional spend until optimisation has been evaluated

---

## Example Scenario 2 — Unapproved AI Coding Assistant

Business request:

```text
A development team wants to paste customer data and
proprietary source code into a new external AI coding
assistant.

The tool has not completed security review but may
improve developer productivity.
```

Coordinator routing:

```text
security_agent
adoption_agent
```

The Security Agent may identify high risk.

The Adoption Agent may still identify a legitimate productivity opportunity.

The Governance Agent must therefore reconcile:

```text
Potential productivity value
            vs
Security / confidentiality risk
```

A suitable recommendation might be:

```text
CONDITIONAL_PILOT

Conditions:
- no customer data
- no proprietary sensitive code
- approved test environment
- security review
- measurable pilot KPIs
- human approval before production rollout
```

---

## Example Scenario 3 — Licence Review

A user may have no recorded activity for an extended period.

The Licence Agent should not automatically recommend deletion.

Instead:

```text
Inactive account detected
        ↓
Review entitlement
        ↓
Check leave / project / role context
        ↓
Validate business requirement
        ↓
Reassign only if justified
        ↓
Human approval
```

This prevents simplistic cost optimisation from creating operational disruption.

---

## Audit Trail

Every completed governance workflow can generate a JSON audit record.

Example:

```text
reports/
└── governance_decision_2026-10-15_19-00-11.json
```

The record can include:

```text
timestamp
request
coordinator_result
capacity_analysis
specialist_results
governance_report
```

This provides traceability between:

```text
Input
→ Routing
→ Calculation
→ Specialist reasoning
→ Final recommendation
```

Generated audit files are excluded from Git through `.gitignore`.

---

## Human-in-the-Loop Governance

The prototype deliberately does not automatically perform high-impact actions.

Examples include:

- removing licences
- increasing budgets
- moving departmental allocation
- approving unreviewed AI vendors
- granting access
- changing security policy

Instead:

```text
Detect
  ↓
Calculate
  ↓
Analyse
  ↓
Recommend
  ↓
Human Approval
  ↓
Approved Action
  ↓
Audit
```

This is a deliberate enterprise governance design choice.

---

## Privacy-Safe Demonstration

This repository uses synthetic demonstration data.

It does not require confidential:

- employee information
- customer records
- production usage data
- internal company datasets

The synthetic data is designed only to demonstrate the architecture and decision patterns.

---

## Project Structure

```text
Enterprise AI Enablement Multi-Agent System/
│
├── agents/
│   ├── __init__.py
│   ├── coordinator.py
│   ├── licence_agent.py
│   ├── finops_agent.py
│   ├── security_agent.py
│   ├── adoption_agent.py
│   └── report_agent.py
│
├── config/
│
├── data/
│   └── department_usage.csv
│
├── reports/
│   └── generated audit records
│
├── capacity_optimizer.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Prototype

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Configure the OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Do not store API keys directly in Python files.

Run:

```bash
python3 main.py
```

The application will prompt:

```text
Enter an AI Enablement request:
>
```

Enter a natural-language governance scenario and the Coordinator will select the relevant specialist agents.

---

## Technology

The prototype currently uses:

- Python
- OpenAI API
- JSON
- CSV
- deterministic governance logic
- multi-agent orchestration
- local audit records

The architecture is intentionally lightweight so that the decision logic remains understandable.

---

## Security

The repository should never contain:

- production API keys
- passwords
- access tokens
- confidential customer information
- internal company secrets
- proprietary production datasets

Secrets should be supplied through environment variables or an approved enterprise secrets-management solution.

---

## Current Limitations

This project is a prototype rather than a production automation platform.

Current limitations include:

- synthetic input data
- simplified forecasting
- no live enterprise telemetry
- no automatic vendor provisioning
- no automatic entitlement changes
- no automatic capacity reallocation
- human approval is represented logically rather than through a real workflow engine
- no persistent database
- no RBAC implementation
- limited automated testing

These limitations are intentional and help separate demonstrated functionality from future production capabilities.

---

## Production Roadmap

A production implementation could add:

1. Vendor usage APIs
2. SSO / SCIM integration
3. HR lifecycle integration
4. Billing and cost APIs
5. Security telemetry
6. Policy-as-code controls
7. Approval workflow integration
8. Teams / Slack notifications
9. Enterprise database storage
10. RBAC
11. Monitoring and alerting
12. Historical forecasting
13. Automated reconciliation
14. Dashboards
15. CI/CD and automated testing
16. Vendor-specific capacity controls

---

## Relationship to Portfolio Project 1

This system complements:

### Enterprise AI Usage, Licence & Cost Governance

Project 1 focuses on:

```text
Observe
→ Measure
→ Forecast
→ Detect
```

Project 2 focuses on:

```text
Route
→ Analyse
→ Optimise
→ Govern
→ Audit
```

Together:

```text
               ENTERPRISE AI ENABLEMENT

Project 1                               Project 2
────────────────────                   ────────────────────
Usage visibility                       Agent orchestration
Licence utilisation                    Specialist reasoning
Cost monitoring                        FinOps interpretation
Department forecasts      ───────►     Capacity optimisation
Anomaly detection                      Security assessment
Governance signals                     Adoption analysis
                                       Final governance decision
                                       Human approval
                                       Audit trail
```

The projects demonstrate how operational telemetry and governance signals could feed a broader enterprise AI decision-support system.

---

## Why This Architecture?

The objective is not to replace operational teams with autonomous agents.

The objective is to explore how AI can support an Enterprise AI Enablement function by helping teams:

- identify the right stakeholders
- analyse competing priorities
- surface risks
- interpret deterministic signals
- optimise existing resources
- produce structured recommendations
- preserve human authority
- maintain traceability

The system therefore follows the principle:

> **Automate analysis where appropriate, preserve deterministic sources of truth, and keep humans accountable for high-impact decisions.**

---

## Portfolio

This repository is part of a two-project Enterprise AI Enablement portfolio:

**Project 1**  
Enterprise AI Usage, Licence & Cost Governance

**Project 2**  
Enterprise AI Enablement Multi-Agent System

Together they demonstrate practical concepts across:

- AI platform operations
- R&D Operations
- AI Enablement
- FinOps
- SaaS administration
- licence management
- security governance
- developer productivity
- responsible AI adoption
- automation
- decision support