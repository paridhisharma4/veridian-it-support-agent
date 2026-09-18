"""
Ticket Management Module
Creates, updates, and retrieves tickets from the ticket queue.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class TicketManager:
    """Manages IT support tickets."""
    
    def __init__(self, tickets_path: str = None):
        """Initialize with tickets file."""
        if tickets_path is None:
            tickets_path = Path(__file__).parent.parent / "data" / "tickets.json"
        
        self.tickets_path = tickets_path
        self._load_tickets()
    
    def _load_tickets(self):
        """Load tickets from file."""
        with open(self.tickets_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tickets = data['tickets']
            self.next_id = data.get('next_ticket_id', 1052)
    
    def _save_tickets(self):
        """Save tickets to file."""
        with open(self.tickets_path, 'w', encoding='utf-8') as f:
            json.dump({
                'tickets': self.tickets,
                'next_ticket_id': self.next_id
            }, f, indent=2, ensure_ascii=False)
    
    def find_matching_ticket(self, employee: str, category: str) -> Optional[Dict]:
        """
        Find an existing open ticket for this employee and category.
        
        Args:
            employee: Employee name
            category: Issue category
            
        Returns:
            Matching ticket or None
        """
        for ticket in self.tickets:
            if (ticket['employee'].lower() == employee.lower() and 
                ticket['category'] == category and
                not ticket.get('closed', False)):
                return ticket
        return None
    
    def create_ticket(self,
                     employee: str,
                     email: str,
                     request_text: str,
                     classification: Dict,
                     kb_result: Dict,
                     decision: Dict) -> Dict:
        """
        Create a new ticket with complete audit trail.
        
        Args:
            employee: Employee name
            email: Employee email
            request_text: Original request text
            classification: Classification result
            kb_result: KB retrieval result
            decision: Decision from engine
            
        Returns:
            Created ticket dict
        """
        ticket_id = f"TK-{self.next_id}"
        self.next_id += 1
        
        # Create issue summary (first 80 chars of request)
        issue_summary = request_text[:77] + "..." if len(request_text) > 80 else request_text
        
        # Determine status based on decision action
        status = self._determine_status(decision['action'], decision.get('escalate_to', ''))
        
        ticket = {
            'id': ticket_id,  # Use 'id' to match existing tickets schema
            'employee': employee,
            'email': email,
            'issue_summary': issue_summary,
            'kb_source_cited': ', '.join(decision.get('kb_sources', [])),
            'status': status,
            'decision_reasoning': decision['reason'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'audit_log': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'step': 'classification',
                    'details': {
                        'category': classification['category'],
                        'confidence': classification['confidence'],
                        'entities': classification['entities'],
                        'reasoning': classification.get('reasoning', '')
                    }
                },
                {
                    'timestamp': datetime.now().isoformat(),
                    'step': 'kb_retrieval',
                    'details': {
                        'policies_found': [p['id'] for p in kb_result['policies']],
                        'conflicts': kb_result['conflicts'],
                        'reasoning': kb_result['reasoning']
                    }
                },
                {
                    'timestamp': datetime.now().isoformat(),
                    'step': 'decision',
                    'details': {
                        'action': decision['action'],
                        'reason': decision['reason'],
                        'reasoning_steps': decision.get('reasoning_steps', []),
                        'escalate_to': decision.get('escalate_to'),
                        'warning': decision.get('warning')
                    }
                }
            ],
            'request_text': request_text
        }
        
        # Add action-specific fields
        if decision.get('escalate_to'):
            ticket['escalate_to'] = decision['escalate_to']
        
        if decision.get('warning'):
            ticket['warning'] = decision['warning']
        
        if decision.get('instructions'):
            ticket['instructions'] = decision['instructions']
        
        if decision.get('precedent'):
            ticket['precedent'] = decision['precedent']
        
        self.tickets.append(ticket)
        self._save_tickets()
        
        return ticket
    
    def update_ticket(self, ticket_id: str, updates: Dict) -> Dict:
        """
        Update an existing ticket.
        
        Args:
            ticket_id: Ticket ID to update
            updates: Dict of fields to update
            
        Returns:
            Updated ticket
        """
        for ticket in self.tickets:
            if ticket['id'] == ticket_id:
                ticket.update(updates)
                ticket['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self._save_tickets()
                return ticket
        
        raise ValueError(f"Ticket {ticket_id} not found")
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get a ticket by ID."""
        for ticket in self.tickets:
            if ticket['id'] == ticket_id:
                return ticket
        return None
    
    def get_all_tickets(self, include_closed: bool = True) -> List[Dict]:
        """Get all tickets, optionally filtering out closed ones."""
        if include_closed:
            return self.tickets
        return [t for t in self.tickets if not t.get('closed', False)]
    
    def get_active_tickets(self) -> List[Dict]:
        """Get only active (non-closed) tickets."""
        return self.get_all_tickets(include_closed=False)
    
    def _determine_status(self, action: str, escalate_to: str = '') -> str:
        """Determine ticket status based on decision action."""
        if action == 'resolve':
            return 'resolved'
        elif action == 'clarify':
            return 'new'  # Waiting for employee response
        elif action == 'escalate':
            if 'security' in escalate_to.lower():
                return 'escalated'
            elif 'finance' in escalate_to.lower():
                return 'in_progress'
            elif 'manager' in escalate_to.lower():
                return 'in_progress'
            else:
                return 'in_progress'
        else:
            return 'new'
