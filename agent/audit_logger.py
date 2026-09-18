"""
Audit Logger Module
Maintains a complete audit trail of all agent decisions and actions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class AuditLogger:
    """Logs all agent actions for audit trail."""
    
    def __init__(self, log_path: str = None):
        """Initialize with audit log file path."""
        if log_path is None:
            log_path = Path(__file__).parent.parent / "data" / "audit_log.jsonl"
        
        self.log_path = log_path
        
        # Create file if it doesn't exist
        if not Path(log_path).exists():
            Path(log_path).touch()
    
    def log_request(self,
                   employee: str,
                   email: str,
                   request_text: str,
                   classification: Dict,
                   kb_policies: List[Dict],
                   conflicts: List[str],
                   decision: Dict,
                   ticket_id: str,
                   clarification_questions: List[str] = None) -> None:
        """
        Log a complete request processing event.
        
        Args:
            employee: Employee name
            email: Employee email
            request_text: Original request
            classification: Intent classification result
            kb_policies: KB articles retrieved
            conflicts: Any policy conflicts
            decision: Decision made by engine
            ticket_id: Created/updated ticket ID
            clarification_questions: Any follow-up questions
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'employee': employee,
            'email': email,
            'request': request_text,
            'classification': {
                'category': classification.get('category'),
                'confidence': classification.get('confidence'),
                'entities': classification.get('entities', {})
            },
            'kb_policies_retrieved': [
                {
                    'id': p['id'],
                    'title': p['title']
                } for p in kb_policies
            ],
            'policy_conflicts': conflicts,
            'decision': {
                'action': decision['action'],
                'reason': decision['reason'],
                'escalate_to': decision.get('escalate_to'),
                'kb_sources': decision.get('kb_sources', [])
            },
            'ticket_id': ticket_id,
            'clarification_questions': clarification_questions or []
        }
        
        # Append to log file (JSONL format - one JSON object per line)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """
        Get recent audit log entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of log entries (most recent first)
        """
        if not Path(self.log_path).exists():
            return []
        
        logs = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        # Return most recent first
        return logs[-limit:][::-1]
    
    def get_logs_for_employee(self, employee: str) -> List[Dict]:
        """Get all log entries for a specific employee."""
        all_logs = self.get_recent_logs(limit=1000)
        return [log for log in all_logs if log['employee'].lower() == employee.lower()]
    
    def get_logs_by_action(self, action: str) -> List[Dict]:
        """Get all log entries with a specific action type."""
        all_logs = self.get_recent_logs(limit=1000)
        return [log for log in all_logs if log['decision']['action'] == action]
