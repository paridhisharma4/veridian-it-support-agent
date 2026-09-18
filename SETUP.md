# Setup Guide - Veridian IT Support Agent

## Quick Setup (2 minutes)

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Streamlit (web interface)
- No ML/LLM libraries needed! (system uses rule-based logic)

**Why so lightweight?**
- The agent uses keyword-based classification (no ML models)
- KB search uses simple keyword matching (no embeddings)
- All reasoning is rule-based (no LLM API calls)
- Result: Fast, offline-capable, no API costs

### 2. Run the Application

```powershell
streamlit run app.py
```

The web interface will automatically open at `http://localhost:8501`

### 3. Test the Agent

You have two options:

**Option A: Use Pre-loaded Requests**
1. Open the sidebar
2. Select one of the 15 pre-loaded employee requests
3. Click "Load Request"
4. Click "Submit Request" to process

**Option B: Enter Custom Request**
1. Fill in employee name and email
2. Enter an IT support request in natural language
3. Click "Submit Request"

### 4. Run Automated Tests (Optional)

```powershell
python tests\test_scenarios.py
```

This will test all 15 employee requests and show results in the console.

## Architecture Overview

The agent follows a pipeline architecture:

```
User Request → Intent Classification → KB Retrieval → Policy Conflict Check 
→ Decision Engine → Ticket Management → Audit Logging → Response
```

### Key Components

- **IntentClassifier** (`agent/classifier.py`): Classifies requests into categories and extracts entities
- **KnowledgeBaseRetriever** (`agent/kb_retrieval.py`): Searches KB articles using keyword matching
- **DecisionEngine** (`agent/decision_engine.py`): Decides to resolve, escalate, or request clarification
- **TicketManager** (`agent/ticket_manager.py`): Creates and manages support tickets
- **AuditLogger** (`agent/audit_logger.py`): Maintains complete audit trail

## Features Demonstrated

✅ **Natural Language Understanding**: Parses free-text requests  
✅ **Knowledge Base Grounding**: All answers cite KB sources  
✅ **Policy Conflict Detection**: Surfaces KB-03 vs Asset Management conflicts  
✅ **Intelligent Escalation**: Routes security incidents, approval-required requests  
✅ **Clarification Questions**: Asks follow-ups for ambiguous requests  
✅ **Ticket Lifecycle**: Creates, updates, tracks tickets  
✅ **Audit Trail**: Complete JSONL log of all decisions  

## Data Files

- `data/knowledge_base.json`: KB articles and policies
- `data/tickets.json`: Ticket queue (pre-seeded with 10 tickets)
- `data/requests.json`: 15 employee requests for testing
- `data/audit_log.jsonl`: Append-only audit log

## Testing Key Scenarios

1. **REQ-01** (Aditi Sharma): Laptop replacement - Should detect policy conflict between KB-03 (3 years) and Asset Management Policy (4 years)

2. **REQ-08** (Ananya Reddy): Security incident - Should escalate immediately to security@veridian-corp.example and warn about forwarding violation

3. **REQ-15** (Rahul Menon): Unclear request - Should ask clarification questions

4. **REQ-02** (Vikram Chawla): Guest Wi-Fi - Should auto-resolve with no approval needed

5. **REQ-11** (Nikhil Bansal): Contractor VPN - Should escalate for manager approval

## Troubleshooting

**Issue**: Import errors  
**Solution**: Make sure you're running from the project root directory

**Issue**: Streamlit won't start  
**Solution**: Check that port 8501 is not already in use

**Issue**: Data files not found  
**Solution**: Ensure you're in the `paridhi_project` directory when running

## Demo Preparation

For the 15-minute demo:

1. **Start with overview** - Show PROJECT.md architecture diagram
2. **Live demo** - Process 3-4 key requests (REQ-01, REQ-08, REQ-15, REQ-02)
3. **Show features**:
   - Policy conflict detection
   - Security escalation
   - Clarification questions
   - Ticket queue
   - Audit trail
4. **Explain grounding** - Show KB sources in responses
5. **Discuss scalability** - How this could integrate with real systems

## Next Steps for Production

- [ ] Integrate with actual HR/employee database
- [ ] Connect to real ticketing system (Jira, ServiceNow)
- [ ] Add LLM integration for more sophisticated NLU (currently using rule-based)
- [ ] Implement vector embeddings for better KB search
- [ ] Add authentication and authorization
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Add email notifications for escalations
- [ ] Implement approval workflows
- [ ] Add reporting and analytics dashboard
