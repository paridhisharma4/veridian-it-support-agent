"""
Veridian IT Support Agent - Streamlit Application
Main web interface for the IT support agent.
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

from agent.classifier import IntentClassifier
from agent.kb_retrieval import KnowledgeBaseRetriever
from agent.decision_engine import DecisionEngine
from agent.ticket_manager import TicketManager
from agent.audit_logger import AuditLogger


# Page configuration
st.set_page_config(
    page_title="Veridian IT Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def get_components():
    """Initialize all agent components."""
    return {
        'classifier': IntentClassifier(),
        'kb_retriever': KnowledgeBaseRetriever(),
        'decision_engine': DecisionEngine(),
        'ticket_manager': TicketManager(),
        'audit_logger': AuditLogger()
    }

components = get_components()

# Load employee requests for testing
@st.cache_data
def load_employee_requests():
    """Load pre-populated employee requests."""
    requests_path = Path(__file__).parent / "data" / "requests.json"
    with open(requests_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['requests']

employee_requests = load_employee_requests()


def process_request(employee_name: str, employee_email: str, request_text: str):
    """
    Process an IT support request through the agent pipeline.
    Returns explicit reasoning trace at each step.
    
    Args:
        employee_name: Name of the employee
        employee_email: Email of the employee
        request_text: The support request text
        
    Returns:
        Dict with processing results and complete reasoning trace
    """
    pipeline_trace = []
    
    # STEP 1: Intent Classification
    pipeline_trace.append("=" * 60)
    pipeline_trace.append("STEP 1: INTENT CLASSIFICATION")
    pipeline_trace.append("=" * 60)
    classification = components['classifier'].classify(request_text)
    pipeline_trace.append(f"Category: {classification['category']}")
    pipeline_trace.append(f"Confidence: {classification['confidence']:.2f}")
    pipeline_trace.append(f"Entities extracted: {classification['entities']}")
    pipeline_trace.append(f"Reasoning: {classification.get('reasoning', '')}")
    pipeline_trace.append("")
    
    # STEP 2: Knowledge Base Retrieval
    pipeline_trace.append("=" * 60)
    pipeline_trace.append("STEP 2: KNOWLEDGE BASE RETRIEVAL")
    pipeline_trace.append("=" * 60)
    kb_result = components['kb_retriever'].search(
        request_text, 
        category=classification['category'],
        top_k=3
    )
    for reason in kb_result['reasoning']:
        pipeline_trace.append(reason)
    pipeline_trace.append(f"KB articles found: {[p['id'] for p in kb_result['policies']]}")
    if kb_result['conflicts']:
        pipeline_trace.append("⚠️ CONFLICTS DETECTED:")
        for conflict in kb_result['conflicts']:
            pipeline_trace.append(f"  - {conflict}")
    pipeline_trace.append("")
    
    # STEP 3: Check if clarification needed
    clarification_questions = []
    if classification['needs_clarification']:
        pipeline_trace.append("=" * 60)
        pipeline_trace.append("STEP 3: CLARIFICATION NEEDED")
        pipeline_trace.append("=" * 60)
        clarification_questions = components['classifier'].generate_clarification_questions(
            classification['category'],
            classification['entities']
        )
        for q in clarification_questions:
            pipeline_trace.append(f"? {q}")
        pipeline_trace.append("")
    
    # STEP 4: Decision Making
    pipeline_trace.append("=" * 60)
    pipeline_trace.append("STEP 4: DECISION ENGINE")
    pipeline_trace.append("=" * 60)
    
    # Get existing tickets for precedent checking
    existing_tickets = components['ticket_manager'].get_all_tickets()
    
    decision = components['decision_engine'].decide(
        classification['category'],
        classification['entities'],
        kb_result,
        existing_tickets
    )
    
    if decision.get('reasoning_steps'):
        for step in decision['reasoning_steps']:
            pipeline_trace.append(step)
    pipeline_trace.append("")
    pipeline_trace.append(f"FINAL DECISION: {decision['action'].upper()}")
    pipeline_trace.append(f"Reason: {decision['reason']}")
    if decision.get('escalate_to'):
        pipeline_trace.append(f"Escalate to: {decision['escalate_to']}")
    pipeline_trace.append("")
    
    # STEP 5: Ticket Creation
    pipeline_trace.append("=" * 60)
    pipeline_trace.append("STEP 5: TICKET MANAGEMENT")
    pipeline_trace.append("=" * 60)
    
    ticket = components['ticket_manager'].create_ticket(
        employee=employee_name,
        email=employee_email,
        request_text=request_text,
        classification=classification,
        kb_result=kb_result,
        decision=decision
    )
    
    pipeline_trace.append(f"Created ticket: {ticket['id']}")
    pipeline_trace.append(f"Status: {ticket['status']}")
    pipeline_trace.append(f"KB sources cited: {ticket['kb_source_cited']}")
    pipeline_trace.append("")
    
    return {
        'classification': classification,
        'kb_result': kb_result,
        'clarification_questions': clarification_questions,
        'decision': decision,
        'ticket': ticket,
        'pipeline_trace': pipeline_trace
    }


def display_response(result: dict):
    """Display the agent's response with complete reasoning trace."""
    
    # Agent Response Header
    st.markdown("### 🤖 Agent Response")
    
    # Decision badge
    action = result['decision']['action']
    if action == 'resolve':
        st.success("✅ **Resolved Automatically**")
    elif action == 'clarify':
        st.info("❓ **Need More Information**")
    elif action == 'escalate':
        if result['decision'].get('conflict_details'):
            st.warning("⚠️ **Policy Conflict Detected - Escalation Required**")
        elif 'security' in result['decision'].get('escalate_to', '').lower():
            st.error("🚨 **Security Escalation - URGENT**")
        else:
            st.warning("📤 **Escalation Required**")
    
    # Warning (if any)
    if 'warning' in result['decision'] and result['decision']['warning']:
        st.error(f"⚠️ **WARNING:** {result['decision']['warning']}")
    
    # Reasoning
    st.markdown("**Decision:**")
    st.write(result['decision']['reason'])
    
    # Instructions
    if 'instructions' in result['decision']:
        st.markdown("**Instructions:**")
        st.info(result['decision']['instructions'])
    
    # Clarification questions
    if result['clarification_questions']:
        st.markdown("**Follow-up Questions:**")
        for i, question in enumerate(result['clarification_questions'], 1):
            st.write(f"{i}. {question}")
    
    # Complete Pipeline Trace
    with st.expander("🔍 Complete Pipeline Trace (Inspectable Reasoning)", expanded=True):
        st.code('\n'.join(result['pipeline_trace']), language='text')
    
    # KB Sources
    if result['decision'].get('kb_sources'):
        with st.expander("📚 Knowledge Base Sources Cited", expanded=False):
            for kb_id in result['decision']['kb_sources']:
                policy = components['kb_retriever'].get_by_id(kb_id)
                if policy:
                    st.markdown(f"**{policy['id']}: {policy['title']}**")
                    st.write(policy['content'])
                    st.divider()
    
    # Policy Conflicts (if any)
    if result['kb_result']['conflicts']:
        with st.expander("⚠️ Policy Conflicts Detected", expanded=True):
            for conflict in result['kb_result']['conflicts']:
                st.warning(conflict)
    
    # Ticket Information
    st.markdown("---")
    st.markdown(f"**Ticket Created:** `{result['ticket']['id']}`")
    st.markdown(f"**Status:** {result['ticket']['status']}")
    st.markdown(f"**KB Sources:** {result['ticket']['kb_source_cited'] or 'None'}")
    
    # Ticket Audit Log
    with st.expander("📋 Ticket Audit Log", expanded=False):
        st.json(result['ticket']['audit_log'])


# Main UI
st.title("🤖 Veridian IT Support Agent")
st.markdown("*AI-powered internal IT support for Veridian Corp employees*")
st.markdown("**Scenario Window:** Monday, 21 September 2026 – Friday, 25 September 2026")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This agent:
    - Understands IT issues from natural language
    - Grounds answers in knowledge base policies
    - Asks clarifying questions when needed
    - Resolves simple requests automatically
    - Escalates complex/risky requests to humans
    - Maintains complete audit trail
    """)
    
    st.divider()
    
    st.header("📋 Quick Test")
    st.markdown("Select a pre-loaded employee request:")
    
    selected_request = st.selectbox(
        "Employee Requests",
        options=[f"{r['id']}: {r['employee']}" for r in employee_requests],
        key="request_selector"
    )
    
    if st.button("Load Request", use_container_width=True):
        idx = int(selected_request.split(':')[0].replace('REQ-', '')) - 1
        req = employee_requests[idx]
        st.session_state.employee_name = req['employee']
        st.session_state.employee_email = req['email']
        st.session_state.request_text = req['request']
        st.rerun()

# Main content area with tabs
tab1, tab2 = st.tabs(["💬 New Request", "🎫 Ticket Queue"])

with tab1:
    st.header("Submit IT Support Request")
    
    col1, col2 = st.columns(2)
    
    with col1:
        employee_name = st.text_input(
            "Employee Name",
            value=st.session_state.get('employee_name', ''),
            placeholder="e.g., John Doe"
        )
    
    with col2:
        employee_email = st.text_input(
            "Employee Email",
            value=st.session_state.get('employee_email', ''),
            placeholder="e.g., john.doe@veridian-corp.example"
        )
    
    request_text = st.text_area(
        "Describe your IT issue",
        value=st.session_state.get('request_text', ''),
        placeholder="e.g., My laptop won't turn on and it's 3 years old",
        height=150
    )
    
    if st.button("Submit Request", type="primary", use_container_width=True):
        if not employee_name or not employee_email or not request_text:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Processing your request..."):
                result = process_request(employee_name, employee_email, request_text)
                st.session_state.last_result = result
                display_response(result)

with tab2:
    st.header("Ticket Queue")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        show_resolved = st.checkbox("Show resolved tickets", value=True)
    with col2:
        if st.button("Refresh", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()
    
    # Get tickets
    all_tickets = components['ticket_manager'].get_all_tickets()
    if not show_resolved:
        tickets = [t for t in all_tickets if t['status'] != 'resolved']
    else:
        tickets = all_tickets
    
    # Display summary
    active_tickets = [t for t in all_tickets if t['status'] != 'resolved']
    st.metric("Active Tickets", len(active_tickets))
    
    st.divider()
    
    # Display tickets
    for ticket in reversed(tickets):  # Most recent first
        status = ticket['status']
        
        # Color code by status
        if status == 'resolved':
            status_color = "🟢"
        elif status == 'escalated' or 'urgent' in status.lower():
            status_color = "🔴"
        elif status == 'in_progress':
            status_color = "🟡"
        else:
            status_color = "🔵"
        
        with st.expander(f"{status_color} {ticket['id']} - {ticket['employee']} - {ticket['issue_summary']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Employee:** {ticket['employee']}")
                st.markdown(f"**Status:** {status}")
                st.markdown(f"**Created:** {ticket.get('created_at', 'N/A')}")
            with col2:
                st.markdown(f"**KB Sources:** {ticket.get('kb_source_cited', 'None')}")
                if ticket.get('escalate_to'):
                    st.markdown(f"**Escalated To:** {ticket['escalate_to']}")
            
            st.markdown(f"**Request:** {ticket.get('request_text', ticket['issue_summary'])}")
            
            if ticket.get('decision_reasoning'):
                st.markdown(f"**Decision Reasoning:** {ticket['decision_reasoning']}")
            
            if ticket.get('warning'):
                st.error(f"⚠️ **WARNING:** {ticket['warning']}")
            
            if ticket.get('instructions'):
                st.info(f"**Instructions:** {ticket['instructions']}")
            
            # Show audit log
            if ticket.get('audit_log'):
                with st.expander("View Audit Log"):
                    st.json(ticket['audit_log'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    Built for AIONOS Agentic AI Factory Hackathon | Veridian Corp IT Support | September 2026
</div>
""", unsafe_allow_html=True)
