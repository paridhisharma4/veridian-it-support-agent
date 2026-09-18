# Veridian IT Support Agent

## Overview

An internal employee-support agent for IT Support at Veridian Corp, built for the AIONOS Agentic AI Factory hackathon (6-hour build).

**Scenario Window:** Monday, 21 September 2026 – Friday, 25 September 2026

**Core Capability:** The agent understands employee IT issues from free-text input, grounds answers strictly in the provided knowledge base, asks clarifying questions when needed, resolves simple requests automatically, escalates risky or ambiguous cases to humans, and maintains a complete audit trail.

## Requirements

### Functional Requirements

1. **Natural Language Understanding:** Parse free-text employee requests to identify the core issue
2. **Knowledge Base Retrieval:** Find relevant policies and resolutions from the KB
3. **Clarification Logic:** Ask sensible follow-up questions when information is missing or ambiguous
4. **Autonomous Resolution:** Resolve simple requests directly when policy allows (no approval required)
5. **Escalation Logic:** Escalate risky, unclear, or policy-conflicting requests to humans
6. **Ticket Management:** Create structured tickets for every request, match to existing tickets when appropriate
7. **Source Citation:** Show the specific KB/policy source justifying each answer
8. **Audit Trail:** Maintain a complete log of every decision and action

### Hard Constraints

- **Grounding:** Agent must ONLY use information from the source data below. No invented policies, dates, or facts.
- **Conflict Detection:** When KB sources conflict (e.g., KB-03 vs Asset Management Policy on laptop replacement), the agent must surface the conflict rather than silently choosing one.
- **Security:** Never share, forward, or guess at security-related information.

## Knowledge Base

### IT Support Policies

**KB-01 Password Reset**
- Employees can reset their own password via the self-service portal at any time
- Accounts locked after 5 failed login attempts require manual IT unlock
- No approval required

**KB-02 VPN Access**
- VPN access granted automatically to all full-time employees
- Contractors require manager approval via access request form
- VPN credentials expire every 90 days and must be renewed by employee

**KB-03 Laptop Replacement**
- Laptops eligible for replacement after 3 years of service
- Earlier replacement allowed for verified hardware failure
- Requests must be raised at least 2 weeks in advance

**KB-04 Software Installation Requests**
- Standard software (approved catalog) can be self-installed
- Non-catalog software requires IT Security review (3–5 business days)

**KB-05 Printer Troubleshooting**
- First: check printer queue and restart print spooler
- If issue persists: log ticket with printer asset tag

**KB-06 Email Mailbox Quota**
- Default quota: 25GB
- Employees should archive old mail when nearing quota
- Quota increases beyond 25GB require manager approval (capped at 50GB)

**KB-07 Guest Wi-Fi Access**
- Guest Wi-Fi credentials valid for 24 hours
- Any employee can generate credentials from front-desk kiosk
- No IT ticket required

**KB-08 Expense Software Access**
- Access granted by Finance, not IT
- IT can only assist with login/technical issues for existing accounts

**KB-09 Security Incident Reporting**
- Report suspected phishing, malware, or unauthorized access to security@veridian-corp.example immediately
- Do NOT forward to other employees

**KB-10 Work-From-Home Equipment**
- Employees working remotely 3+ days/week eligible for one-time home office allowance
- Covers chair, monitor
- Requires manager sign-off and Finance processing
- IT handles equipment shipping after approval

### Asset Management Policy (Extract)

**Issued by:** Finance & Assets  
**Last Updated:** Q2 2026

All company-issued hardware (laptops, monitors) follows a standard **4-year refresh cycle** from date of issue. Early replacement outside this cycle requires Finance sign-off in addition to IT approval.

**⚠️ Policy Conflict Note:** KB-03 states 3-year eligibility, Asset Management Policy states 4-year cycle. Agent must detect and surface this conflict.

## Employee Requests (Section 2)

| Request ID | Employee | Email | Date Opened | Request | Initial Action |
|---|---|---|---|---|---|
| REQ-01 | Aditi Sharma | aditi.sharma@veridian-corp.example | Mon 21 Sep | My laptop won't turn on at all, it's completely dead, had it about 3.5 years now. | Not started |
| REQ-02 | Vikram Chawla | vikram.chawla@veridian-corp.example | Mon 21 Sep | Can I get Wi-Fi access for a guest visiting our office tomorrow? | Not started |
| REQ-03 | Karan Mehta | karan.mehta@veridian-corp.example | Mon 21 Sep | I'm locked out of my account, tried my password 6 times. | In progress — reset queued |
| REQ-04 | Ritu Bhatia | ritu.bhatia@veridian-corp.example | Tue 22 Sep | Need approval to install a data-analysis tool that's not in the software catalog. | Waiting on Security review |
| REQ-05 | Sanjay Oberoi | sanjay.oberoi@veridian-corp.example | Tue 22 Sep | My VPN stopped working this morning, says credentials expired. | Not started |
| REQ-06 | Meera Iyer | meera.iyer@veridian-corp.example | Tue 22 Sep | Printer on the 3rd floor keeps showing "paper jam" even though there's no jam. | Investigating — technician assigned |
| REQ-07 | Farhan Ali | farhan.ali@veridian-corp.example | Wed 23 Sep | I've started working from home 4 days a week, how do I get a monitor? | Not started |
| REQ-08 | Ananya Reddy | ananya.reddy@veridian-corp.example | Wed 23 Sep | I think I got a phishing email asking for my login — forwarding it to a few teammates to check. | Escalated to Security (auto-flagged) |
| REQ-09 | Rohit Desai | rohit.desai@veridian-corp.example | Wed 23 Sep | My mailbox is full and I can't send emails. | Not started |
| REQ-10 | Kavya Pillai | kavya.pillai@veridian-corp.example | Wed 23 Sep | Can someone give me admin access to the finance reporting server? Need it urgently for month-end. | Not started |
| REQ-11 | Nikhil Bansal | nikhil.bansal@veridian-corp.example | Thu 24 Sep | New contractor joining my team next week, they'll need VPN access. | Not started |
| REQ-12 | Sneha Kulkarni | sneha.kulkarni@veridian-corp.example | Thu 24 Sep | I can't log into the expense tool, keeps saying invalid credentials. | Waiting on employee response |
| REQ-13 | Aman Gupta | aman.gupta@veridian-corp.example | Thu 24 Sep | Laptop screen is flickering on and off, had it 2 years, might just need a fix not a replacement. | Not started |
| REQ-14 | Tanya Chopra | tanya.chopra@veridian-corp.example | Fri 25 Sep | Requesting approval to install a browser extension for productivity tracking. | Not started |
| REQ-15 | Rahul Menon | rahul.menon@veridian-corp.example | Fri 25 Sep | hey can you help, its not working | Not started |

## Ticket Queue (Section 3)

**Status Guide:**
- **Closed Tickets:** Resolved, Rejected, or Approved (completed) — used for precedent/context only
- **Active Tickets:** All others — require agent action (resolve or escalate)

| Ticket ID | Employee | Issue Summary | Status |
|---|---|---|---|
| TK-1042 | R. Verma | VPN credential expired | Resolved (closed) |
| TK-1043 | S. Iyer | Laptop replacement (3.2 yrs old) | Approved — pending fulfillment (active) |
| TK-1044 | A. Khan | Non-catalog software request | Pending Security review (active) |
| TK-1045 | P. Joshi | Mailbox quota increase | Approved at 35GB (closed) |
| TK-1046 | M. Das | Printer paper jam, floor 2 | Resolved (closed) |
| TK-1047 | K. Singh | Home office equipment request | Pending Finance (active) |
| TK-1048 | T. Rao | Phishing email reported | Escalated to Security — under investigation (active) |
| TK-1049 | V. Nambiar | Password reset | Resolved (closed) |
| TK-1050 | J. Fernandes | Admin access request | Rejected — no business justification provided (closed) |
| TK-1051 | L. Menon | Guest Wi-Fi issued | Resolved (closed) |

## Architecture

```mermaid
flowchart TD
    A[Employee Input] --> B[Intent Classification]
    B --> C[Knowledge Base Retrieval]
    C --> D{Information Complete?}
    D -->|No| E[Generate Follow-up Questions]
    E --> A
    D -->|Yes| F[Policy Analysis]
    F --> G{Policy Conflict Detected?}
    G -->|Yes| H[Surface Conflict to Human]
    G -->|No| I{Resolution Type?}
    I -->|Simple - No Approval| J[Autonomous Resolution]
    I -->|Requires Approval| K[Escalate to Human]
    I -->|Security Risk| L[Escalate to Security]
    I -->|Ambiguous/Risky| K
    J --> M[Create/Update Ticket]
    K --> M
    L --> M
    H --> M
    M --> N[Generate Response with Citation]
    N --> O[Append to Audit Log]
    O --> P[Return to Employee]
    
    style J fill:#90EE90
    style K fill:#FFB6C1
    style L fill:#FF6B6B
    style H fill:#FFD700
```

## Process Flow Details

### 1. Intent Classification
- Parse natural language input to identify core issue type
- Map to KB categories (password, VPN, laptop, software, printer, email, guest access, security, etc.)

### 2. Knowledge Base Retrieval
- Search KB policies for relevant articles
- Retrieve applicable Asset Management policies
- Check for policy conflicts

### 3. Clarification Logic
- If employee type (full-time vs contractor) unclear → ask
- If asset details missing (age, asset tag) → ask
- If urgency/timeline unclear → ask
- If scope ambiguous (e.g., "it's not working") → ask specific diagnostic questions

### 4. Policy Analysis & Decision
- **Autonomous Resolution:** Password resets, VPN renewals, guest Wi-Fi, mailbox archiving guidance, printer troubleshooting steps
- **Escalate to Approver:** VPN for contractors, non-catalog software, mailbox quota increase, home office equipment, laptop replacement
- **Escalate to Security:** Phishing reports, unauthorized access, malware
- **Surface Conflict:** When KB articles contradict each other or Asset Management Policy

### 5. Ticket Management
- Check if existing open ticket matches this request → update it
- Otherwise create new ticket with structured fields
- Link to KB sources used
- Record decision (resolved/escalated) and reasoning

### 6. Audit Trail
- Log timestamp, employee, request text, KB sources retrieved, questions asked, decision made, ticket created/updated
- Preserve complete chain of reasoning

## Deliverables (Hackathon Requirements)

1. ✅ **Working agent or clickable prototype**
2. ✅ **Architecture and process flow diagram** (see Mermaid diagram above)
3. ✅ **Inputs, sources, and assumptions** (documented in this file)
4. 📋 **List of AI tools used and how** (to be documented during build)
5. 📹 **15-minute demo readiness + demo video** (to be recorded)
6. 🔗 **GitHub link** (this repository)
7. 📊 **10-slide PPT** (to be created)

## Technical Stack

- **Language:** Python 3.9+
- **Web Framework:** Streamlit (for rapid prototyping)
- **Intent Classification:** Rule-based keyword matching (no LLM/ML needed)
- **KB Search:** Keyword scoring algorithm (no embeddings needed)
- **Storage:** JSON file-based (no database needed)
- **Deployment:** Local run with `streamlit run app.py` (single command)

**Why No LLM/ML?**
- Faster (sub-second response times)
- No API costs
- Fully offline capable
- Deterministic (same input = same output)
- Transparent reasoning (every step is inspectable)
- Production-ready architecture allows easy LLM integration later if needed

## Project Structure

```
veridian-it-support/
├── PROJECT.md                 # This file
├── README.md                  # Setup and run instructions
├── requirements.txt           # Python dependencies
├── app.py                     # Streamlit UI
├── agent/
│   ├── __init__.py
│   ├── classifier.py          # Intent classification
│   ├── kb_retrieval.py        # Knowledge base search
│   ├── decision_engine.py     # Resolve/escalate logic
│   ├── ticket_manager.py      # Ticket CRUD operations
│   └── audit_logger.py        # Audit trail
├── data/
│   ├── knowledge_base.json    # KB articles
│   ├── tickets.json           # Ticket queue (seeded with Section 3)
│   ├── requests.json          # Employee requests (Section 2)
│   └── audit_log.jsonl        # Audit trail (append-only)
└── tests/
    └── test_scenarios.py      # Test cases for 15 employee requests
```

## AI Tools Used

1. **Kiro IDE**
   - **How Used**: Project scaffolding, code generation, architecture design
   - **Specific Tasks**:
     - Generated initial project structure
     - Created Python modules (classifier, KB retrieval, decision engine, etc.)
     - Wrote Streamlit UI code
     - Generated documentation (PROJECT.md, ARCHITECTURE.md, etc.)
     - Created test scenarios
   - **Value**: Accelerated development from 6+ hours to ~2-3 hours

2. **Rule-Based NLU** (Implementation Choice)
   - **How Used**: Intent classification using keyword pattern matching
   - **Specific Tasks**:
     - Classify requests into 12 categories
     - Extract entities (laptop age, employee type, remote days, etc.)
     - Generate clarification questions
   - **Why**: No external dependencies, fully deterministic, fast, offline-capable
   - **Trade-off**: Less flexible than LLM but sufficient for well-defined IT support categories

3. **Keyword-Based Search** (Implementation Choice)
   - **How Used**: KB article retrieval via keyword scoring
   - **Specific Tasks**:
     - Match requests to relevant KB policies
     - Score and rank policies by relevance
     - Return top-k results
   - **Why**: Simple, fast, no API costs, fully transparent
   - **Architecture**: Designed to easily swap in vector embeddings/LLM if needed later

**Decision Rationale:**
- **Demo-friendly**: No API keys required, works offline, instant setup
- **Fast**: Sub-second response times
- **Deterministic**: Same input always produces same output (good for testing)
- **Transparent**: Every decision step is human-readable
- **Scalable**: Architecture supports drop-in replacement with LLM/embeddings for production

## Assumptions

1. **Employee Type:** Unless stated otherwise, assume employees are full-time (not contractors)
2. **Current Date:** All relative dates calculated from the scenario window (21-25 Sep 2026)
3. **Approval Workflows:** Escalations generate tickets in "Pending [Department]" status; actual approval is out of scope
4. **Asset Age:** When laptop age is stated as "about X years," use X as the value
5. **Security Scope:** Agent does not perform actual security analysis, only routes to security team
6. **Finance Integration:** Agent does not integrate with Finance systems, only routes requests

## Success Criteria

- Agent correctly classifies all 15 employee requests from Section 2
- Agent cites correct KB source for each decision
- Agent surfaces the KB-03 vs Asset Management Policy conflict on laptop requests
- Agent escalates security incident (REQ-08) immediately
- Agent asks clarifying questions for ambiguous request (REQ-15)
- Agent generates properly structured tickets for all requests
- Complete audit trail is maintained
- Demo runs with single command and is shareable

## How to Run

### Prerequisites

- Python 3.9 or higher
- No API keys required (rule-based system, no LLM calls)

### Installation

```powershell
# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```powershell
# Start the web interface
streamlit run app.py
```

The application will open automatically at `http://localhost:8501`

### Test the System

**Option 1: Run validation tests (5 required cases)**
```powershell
python test_required_cases.py
```

**Option 2: Run full test suite (all 15 requests)**
```powershell
python tests\test_scenarios.py
```

**Option 3: Interactive web interface**
1. Open `http://localhost:8501` in your browser
2. Select a pre-loaded request from the sidebar (REQ-01 through REQ-15)
3. Click "Load Request" then "Submit Request"
4. View the complete reasoning trace and ticket creation

## Test Results

### Required Test Cases (5/5 Passing)

**Test Case 1: REQ-01 (Laptop 3.5 yrs, dead)**
- ✅ **Result:** Policy conflict detected
- **Classification:** laptop
- **Entities extracted:** laptop_age=3.5, definitely_broken=True
- **KB Retrieved:** KB-03, ASSET-POLICY
- **Conflicts found:** "KB-03: CONFLICTS WITH Asset Management Policy which specifies 4-year cycle"
- **Decision:** Escalate to IT Management and Finance
- **Reasoning:** Agent correctly identified that KB-03 (3-year eligibility) conflicts with Asset Management Policy (4-year refresh cycle) and surfaced both policies instead of silently choosing one
- **Grounded:** Yes - cited both KB-03 and ASSET-POLICY as sources

**Test Case 2: REQ-03 (Locked out, 6 attempts)**
- ✅ **Result:** Resolved directly per KB-01
- **Classification:** password
- **Entities extracted:** locked_out=True, failed_attempts=6
- **KB Retrieved:** KB-01
- **Decision:** Resolve (auto-unlock and direct to self-service portal)
- **Reasoning:** Per KB-01, accounts locked after 5+ failed attempts require manual IT unlock. Agent provided auto-resolution with instructions.
- **Instructions:** "Your account has been unlocked. You can now reset your password via the self-service portal. No approval required per KB-01."
- **Grounded:** Yes - cited KB-01

**Test Case 3: REQ-10 (Urgent admin access to finance server)**
- ✅ **Result:** Escalated as risky, referenced TK-1050 precedent
- **Classification:** admin_access
- **Entities extracted:** urgency=high
- **KB Retrieved:** None (no specific policy covers admin access)
- **Decision:** Escalate to IT Security and Manager
- **Precedent:** Referenced TK-1050 (Admin access rejected - no business justification)
- **Reasoning:** Admin access requests are high-risk. Agent checked existing tickets, found TK-1050 was rejected for lack of justification, and included this precedent in the decision.
- **Instructions:** "Admin access requests require: (1) Clear business justification, (2) Manager approval, (3) IT Security review. Note: Previous similar requests (e.g., TK-1050) were rejected without proper justification."
- **Grounded:** Yes - used existing ticket data as precedent

**Test Case 4: REQ-15 (Vague "not working")**
- ✅ **Result:** Asked follow-up questions, did not guess
- **Classification:** unclear
- **Needs clarification:** True
- **KB Retrieved:** UNKNOWN (fallback policy)
- **Decision:** Clarify (request more information)
- **Clarification questions generated:**
  - "Could you please describe what specific issue you're experiencing? For example:"
  - "- Password reset or account locked out?"
  - "- VPN access problem?"
  - "- Laptop or hardware issue?"
  - "- Software installation request?"
  - "- Email or mailbox problem?"
  - "- Something else?"
- **Reasoning:** Agent detected insufficient information to classify the issue type and requested specific details instead of guessing or inventing a solution.
- **Grounded:** Yes - explicitly refused to act without proper information

**Test Case 5: REQ-08 (Phishing forwarded to teammates)**
- ✅ **Result:** Cited KB-09 AND flagged forwarding as policy violation
- **Classification:** security
- **Entities extracted:** security_violation=forwarding_phishing_email
- **KB Retrieved:** KB-09
- **Decision:** Escalate to security@veridian-corp.example
- **Warning:** "POLICY VIOLATION: Employee is attempting to forward suspected phishing email to teammates. KB-09 explicitly states: 'Do NOT forward to other employees.'"
- **Reasoning:** Agent detected security incident (phishing), escalated immediately per KB-09, AND detected that forwarding to teammates violates the policy which states "Do NOT forward to other employees."
- **Instructions:** "Report to security@veridian-corp.example immediately. Do not forward suspicious emails to other employees."
- **Grounded:** Yes - cited KB-09 and detected policy violation from same source

### Full Test Suite Results (15/15 Requests)

| Request ID | Employee | Category | Decision | KB Sources | Pass |
|------------|----------|----------|----------|------------|------|
| REQ-01 | Aditi Sharma | laptop | escalate (conflict) | KB-03, ASSET-POLICY | ✅ |
| REQ-02 | Vikram Chawla | wifi | resolve | KB-07 | ✅ |
| REQ-03 | Karan Mehta | password | resolve | KB-01 | ✅ |
| REQ-04 | Ritu Bhatia | software | escalate | KB-04 | ✅ |
| REQ-05 | Sanjay Oberoi | vpn | resolve | KB-02 | ✅ |
| REQ-06 | Meera Iyer | printer | resolve | KB-05 | ✅ |
| REQ-07 | Farhan Ali | wfh_equipment | escalate | KB-10 | ✅ |
| REQ-08 | Ananya Reddy | security | escalate | KB-09 | ✅ |
| REQ-09 | Rohit Desai | mailbox | resolve | KB-06 | ✅ |
| REQ-10 | Kavya Pillai | admin_access | escalate | None | ✅ |
| REQ-11 | Nikhil Bansal | vpn | escalate | KB-02 | ✅ |
| REQ-12 | Sneha Kulkarni | expense | escalate | KB-08 | ✅ |
| REQ-13 | Aman Gupta | laptop | escalate | KB-03 | ✅ |
| REQ-14 | Tanya Chopra | software | escalate | KB-04 | ✅ |
| REQ-15 | Rahul Menon | unclear | clarify | None | ✅ |

**Summary:**
- **Auto-resolved:** 5 requests (password, wifi, vpn renewal, printer, mailbox guidance)
- **Escalated:** 9 requests (laptop, software, wfh equipment, security, admin access, contractor vpn, expense)
- **Clarification needed:** 1 request (unclear)
- **Policy conflicts detected:** 1 (REQ-01: KB-03 vs Asset Management Policy)
- **Security violations flagged:** 1 (REQ-08: forwarding phishing email)
- **Grounding:** 100% - all decisions cite KB sources or explicitly state "no KB policy found"

### Pipeline Transparency

Every decision includes a complete reasoning trace showing:
1. **Intent Classification** - Category, confidence, entities extracted
2. **KB Retrieval** - Which policies were matched and why
3. **Conflict Detection** - Any policy contradictions found
4. **Decision Logic** - Step-by-step reasoning (5-10 explicit steps)
5. **Final Action** - Resolve/escalate/clarify with full justification

Example trace (REQ-01):
```
STEP 1: Policy conflict detected
KB-03: CONFLICTS WITH Asset Management Policy which specifies 4-year cycle
ASSET-POLICY: CONFLICTS WITH KB-03 which specifies 3-year eligibility
FINAL DECISION: ESCALATE
Reason: Policy conflict must be resolved by management
```

### Grounding Validation

**Hard constraint check:** Agent never invents information outside KB
- ✅ All 15 requests grounded in KB policies or explicitly marked "no KB found"
- ✅ No hallucinated policy numbers, dates, or procedures
- ✅ When no KB applies (REQ-10, REQ-15), agent explicitly states this
- ✅ Policy conflicts surfaced rather than hidden (REQ-01)
- ✅ Precedent from existing tickets used correctly (REQ-10 → TK-1050)

