"""
Test Scenarios for Veridian IT Support Agent
Tests all 15 employee requests from the assignment.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.classifier import IntentClassifier
from agent.kb_retrieval import KnowledgeBaseRetriever
from agent.decision_engine import DecisionEngine
from agent.ticket_manager import TicketManager
from agent.audit_logger import AuditLogger
import json


def load_test_requests():
    """Load employee requests from data file."""
    requests_path = Path(__file__).parent.parent / "data" / "requests.json"
    with open(requests_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['requests']


def test_request(request_data, components):
    """Test a single request through the agent pipeline."""
    print(f"\n{'='*80}")
    print(f"Testing {request_data['id']}: {request_data['employee']}")
    print(f"Request: {request_data['request']}")
    print(f"{'='*80}\n")
    
    # Classify
    classification = components['classifier'].classify(request_data['request'])
    print(f"Classification: {classification['category']} (confidence: {classification['confidence']:.2f})")
    print(f"Entities: {classification['entities']}")
    
    # Retrieve KB
    kb_result = components['kb_retriever'].search(
        request_data['request'], 
        category=classification['category'],
        top_k=3
    )
    print(f"\nKB Policies Retrieved:")
    for policy in kb_result['policies']:
        print(f"  - {policy['id']}: {policy['title']}")
    
    # Check conflicts
    if kb_result['conflicts']:
        print(f"\nCONFLICTS DETECTED:")
        for conflict in kb_result['conflicts']:
            print(f"  - {conflict}")
    
    # Generate clarifications if needed
    if classification['needs_clarification']:
        questions = components['classifier'].generate_clarification_questions(
            classification['category'],
            classification['entities']
        )
        print(f"\nClarification Questions:")
        for q in questions:
            print(f"  ? {q}")
    
    # Make decision
    existing_tickets = components['ticket_manager'].get_all_tickets()
    decision = components['decision_engine'].decide(
        classification['category'],
        classification['entities'],
        kb_result,
        existing_tickets
    )
    print(f"\nDecision: {decision['action']}")
    print(f"Reason: {decision['reason']}")
    if 'escalate_to' in decision:
        print(f"Escalate To: {decision['escalate_to']}")
    if 'instructions' in decision:
        print(f"Instructions: {decision['instructions'][:100]}...")
    if 'warning' in decision:
        print(f"WARNING: {decision['warning']}")
    
    print(f"\nKB Sources: {decision.get('kb_sources', [])}")
    
    if decision.get('reasoning_steps'):
        print(f"\nReasoning Steps:")
        for step in decision['reasoning_steps'][:5]:  # Show first 5 steps
            print(f"  {step}")
    
    return {
        'request_id': request_data['id'],
        'classification': classification,
        'decision': decision,
        'conflicts': kb_result['conflicts']
    }


def main():
    """Run all test scenarios."""
    print("="*80)
    print("VERIDIAN IT SUPPORT AGENT - TEST SCENARIOS")
    print("="*80)
    
    # Initialize components
    components = {
        'classifier': IntentClassifier(),
        'kb_retriever': KnowledgeBaseRetriever(),
        'decision_engine': DecisionEngine(),
        'ticket_manager': TicketManager(),
        'audit_logger': AuditLogger()
    }
    
    # Load test requests
    requests = load_test_requests()
    
    # Test each request
    results = []
    for request_data in requests:
        result = test_request(request_data, components)
        results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    action_counts = {}
    for result in results:
        action = result['decision']['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    print("\nActions Taken:")
    for action, count in sorted(action_counts.items()):
        print(f"  {action}: {count}")
    
    print(f"\nTotal Requests Processed: {len(results)}")
    
    # Highlight important cases
    print("\n" + "="*80)
    print("KEY VALIDATIONS")
    print("="*80)
    
    # Check REQ-08 (security incident)
    req08 = next(r for r in results if r['request_id'] == 'REQ-08')
    if req08['decision']['action'] == 'escalate' and 'security' in req08['decision'].get('escalate_to', '').lower():
        print("[PASS] REQ-08: Security incident correctly escalated")
    else:
        print("[FAIL] REQ-08: Security incident NOT escalated!")
    
    # Check REQ-01 (laptop replacement with conflict)
    req01 = next(r for r in results if r['request_id'] == 'REQ-01')
    if req01['conflicts']:
        print("[PASS] REQ-01: Policy conflict detected (KB-03 vs Asset Management)")
    else:
        print("[WARN] REQ-01: Policy conflict not detected")
    
    # Check REQ-15 (unclear request)
    req15 = next(r for r in results if r['request_id'] == 'REQ-15')
    if req15['classification']['needs_clarification'] or req15['decision']['action'] == 'clarify':
        print("[PASS] REQ-15: Unclear request identified, clarification requested")
    else:
        print("[FAIL] REQ-15: Unclear request not handled properly")
    
    # Check REQ-03 (guest wifi - auto resolve - actually it's password reset)
    req03 = next(r for r in results if r['request_id'] == 'REQ-03')
    if req03['decision']['action'] == 'resolve':
        print("[PASS] REQ-03: Password reset auto-resolved correctly")
    else:
        print("[WARN] REQ-03: Password reset not auto-resolved")


if __name__ == '__main__':
    main()
