# Veridian IT Support Agent

An AI-powered internal IT support agent for Veridian Corp that understands employee issues, grounds answers in policy, and maintains complete audit trails.

## Quick Start

### Prerequisites

- Python 3.9 or higher
- **No API keys needed** (rule-based system, no LLM calls)
- **No ML libraries** (torch, transformers, etc. not required)

### Installation

1. Clone this repository
2. Install dependencies (just Streamlit):
   ```powershell
   pip install -r requirements.txt
   ```

   **Note:** This is a lightweight install (only Streamlit + standard library). No heavy ML dependencies.

3. Run the agent:
   ```powershell
   streamlit run app.py
   ```

The web interface will open at `http://localhost:8501`

## Usage

1. Enter an IT support request in natural language (e.g., "My laptop won't turn on and it's 3 years old")
2. The agent will:
   - Classify your intent
   - Search the knowledge base
   - Ask clarifying questions if needed
   - Provide a resolution or escalation with KB citation
   - Create/update a ticket
   - Log the full audit trail

3. View all tickets in the "Ticket Queue" section
4. Review the audit log in the "Audit Trail" section

## Testing with Sample Requests

The system is pre-loaded with 15 employee requests from the assignment brief. You can test the agent with these or enter your own requests.

## Features

- ✅ Natural language understanding
- ✅ Knowledge base retrieval with semantic search
- ✅ Policy conflict detection (KB-03 vs Asset Management Policy)
- ✅ Intelligent escalation logic
- ✅ Security incident auto-routing
- ✅ Ticket creation and matching
- ✅ Complete audit trail
- ✅ Source citation for all decisions

## Project Structure

```
├── PROJECT.md              # Full project specification
├── README.md               # This file
├── requirements.txt        # Dependencies
├── app.py                  # Streamlit web interface
├── agent/
│   ├── classifier.py       # Intent classification
│   ├── kb_retrieval.py     # Knowledge base search
│   ├── decision_engine.py  # Resolve/escalate logic
│   ├── ticket_manager.py   # Ticket management
│   └── audit_logger.py     # Audit logging
└── data/
    ├── knowledge_base.json # KB articles and policies
    ├── tickets.json        # Ticket queue
    ├── requests.json       # Pre-loaded employee requests
    └── audit_log.jsonl     # Audit trail (append-only)
```

## Demo Video

[Link to demo video will be added here]

## Deliverables

- ✅ Working prototype (this application)
- ✅ Architecture diagram (see PROJECT.md)
- ✅ Documentation (PROJECT.md + this README)
- 📹 Demo video (to be recorded)
- 📊 Presentation slides (to be created)

## License

Built for AIONOS Agentic AI Factory Hackathon Assignment
