"""
Quick test to verify ticket creation uses correct 'id' key.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.classifier import IntentClassifier
from agent.kb_retrieval import KnowledgeBaseRetriever
from agent.decision_engine import DecisionEngine
from agent.ticket_manager import TicketManager


def test_req01():
    """Test REQ-01 end-to-end to verify ticket key is correct."""
    print("Testing REQ-01 (Aditi Sharma) end-to-end...")
    
    request = "My laptop won't turn on at all, it's completely dead, had it about 3.5 years now."
    employee = "Aditi Sharma"
    email = "aditi.sharma@veridian-corp.example"
    
    # Initialize components
    classifier = IntentClassifier()
    kb_retriever = KnowledgeBaseRetriever()
    decision_engine = DecisionEngine()
    ticket_mgr = TicketManager()
    
    # Run pipeline
    print("\n1. Classifying...")
    classification = classifier.classify(request)
    print(f"   Category: {classification['category']}")
    
    print("\n2. Retrieving KB...")
    kb_result = kb_retriever.search(request, category=classification['category'])
    print(f"   Found: {[p['id'] for p in kb_result['policies']]}")
    print(f"   Conflicts: {len(kb_result['conflicts'])} detected")
    
    print("\n3. Making decision...")
    decision = decision_engine.decide(
        classification['category'],
        classification['entities'],
        kb_result,
        ticket_mgr.get_all_tickets()
    )
    print(f"   Action: {decision['action']}")
    
    print("\n4. Creating ticket...")
    ticket = ticket_mgr.create_ticket(
        employee=employee,
        email=email,
        request_text=request,
        classification=classification,
        kb_result=kb_result,
        decision=decision
    )
    
    print(f"   Ticket created: {ticket['id']}")
    print(f"   Status: {ticket['status']}")
    print(f"   Employee: {ticket['employee']}")
    print(f"   KB sources: {ticket['kb_source_cited']}")
    
    # Verify key structure
    print("\n5. Verifying ticket structure...")
    required_keys = ['id', 'employee', 'email', 'issue_summary', 'status', 'kb_source_cited', 'created_at', 'audit_log']
    missing_keys = [k for k in required_keys if k not in ticket]
    
    if missing_keys:
        print(f"   [FAIL] Missing keys: {missing_keys}")
        return False
    
    # Check that 'ticket_id' is NOT present (should be 'id')
    if 'ticket_id' in ticket:
        print(f"   [FAIL] Found 'ticket_id' key - should be 'id'")
        return False
    
    print(f"   [PASS] All required keys present, using 'id' (not 'ticket_id')")
    
    # Test UI access pattern
    print("\n6. Testing UI access pattern...")
    try:
        ticket_display = f"{ticket['id']} - {ticket['employee']} - {ticket['issue_summary']}"
        print(f"   Display string: {ticket_display}")
        print(f"   [PASS] UI can access ticket['id']")
    except KeyError as e:
        print(f"   [FAIL] KeyError: {e}")
        return False
    
    print("\n[SUCCESS] REQ-01 test passed! Ticket creation works correctly.")
    return True


if __name__ == '__main__':
    success = test_req01()
    sys.exit(0 if success else 1)
