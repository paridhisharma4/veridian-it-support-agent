"""
Decision Engine Module
Determines whether to resolve, escalate, or request more information.
Makes explicit, traceable decisions based on KB policies and request context.
"""

from typing import Dict, List


class DecisionEngine:
    """Makes resolve/escalate decisions based on KB policies and request context."""
    
    # Categories that can be auto-resolved (no approval needed)
    AUTO_RESOLVE_CATEGORIES = ['password', 'wifi', 'printer']
    
    def decide(self, 
               category: str, 
               entities: Dict, 
               kb_result: Dict,
               existing_tickets: List[Dict] = None) -> Dict:
        """
        Make a decision on how to handle the request.
        Returns explicit reasoning trace.
        
        Args:
            category: Intent category
            entities: Extracted entities
            kb_result: Result from KB retrieval (policies, conflicts, reasoning)
            existing_tickets: List of existing tickets for precedent checking
            
        Returns:
            Decision dict with action, reasoning trace, and relevant info
        """
        policies = kb_result['policies']
        conflicts = kb_result['conflicts']
        reasoning_steps = []
        
        # Step 1: Check for policy conflicts FIRST
        if conflicts:
            reasoning_steps.append("STEP 1: Policy conflict detected")
            reasoning_steps.extend(conflicts)
            primary_policy = policies[0] if policies else None
            
            return {
                'action': 'escalate',
                'escalate_to': 'IT Management and Finance',
                'reason': 'Policy conflict must be resolved by management',
                'kb_sources': [p['id'] for p in policies],
                'instructions': 'Two policies conflict on this issue. Both KB-03 (3-year laptop replacement) and Asset Management Policy (4-year refresh cycle) apply. Management must clarify which policy takes precedence.',
                'reasoning_steps': reasoning_steps,
                'conflict_details': conflicts
            }
        
        # Step 2: Check for security incidents
        if category == 'security':
            reasoning_steps.append("STEP 2: Security incident detected")
            policy = policies[0] if policies else None
            
            # Check for policy violation
            violation_warning = None
            if entities.get('security_violation') == 'forwarding_phishing_email':
                violation_warning = "POLICY VIOLATION: Employee is attempting to forward suspected phishing email to teammates. KB-09 explicitly states: 'Do NOT forward to other employees.'"
                reasoning_steps.append(violation_warning)
            
            reasoning_steps.append(f"Action: Escalate immediately to security@veridian-corp.example per {policy['id'] if policy else 'KB-09'}")
            
            return {
                'action': 'escalate',
                'escalate_to': 'security@veridian-corp.example',
                'reason': 'Security incident requires immediate escalation per KB-09',
                'kb_sources': [policy['id']] if policy else ['KB-09'],
                'instructions': 'Report to security@veridian-corp.example immediately. Do not forward suspicious emails to other employees.',
                'reasoning_steps': reasoning_steps,
                'warning': violation_warning
            }
        
        # Step 3: Handle unclear requests
        if category == 'unclear':
            reasoning_steps.append("STEP 3: Request is too vague to classify")
            reasoning_steps.append("Action: Request clarification from employee")
            
            return {
                'action': 'clarify',
                'reason': 'Request lacks sufficient detail to identify the issue',
                'kb_sources': [],
                'reasoning_steps': reasoning_steps
            }
        
        # Step 4: Check if we have a valid KB policy
        primary_policy = policies[0] if policies else None
        if not primary_policy or primary_policy['id'] == 'UNKNOWN':
            reasoning_steps.append("STEP 4: No KB policy found for this request")
            reasoning_steps.append("Action: Escalate to IT Management for review")
            
            return {
                'action': 'escalate',
                'escalate_to': 'IT Management',
                'reason': 'No matching KB policy found - requires human review',
                'kb_sources': [],
                'reasoning_steps': reasoning_steps
            }
        
        reasoning_steps.append(f"STEP 4: Found relevant policy - {primary_policy['id']}: {primary_policy['title']}")
        
        # Step 5: Category-specific decision logic
        reasoning_steps.append("STEP 5: Applying policy rules")
        
        # PASSWORD RESET
        if category == 'password':
            if entities.get('locked_out'):
                reasoning_steps.append(f"- Employee locked out after {entities.get('failed_attempts', '5+')} failed attempts")
                reasoning_steps.append("- Per KB-01: Account must be manually unlocked by IT")
                reasoning_steps.append("- Decision: Auto-resolve (unlock account, direct to self-service portal)")
                
                return {
                    'action': 'resolve',
                    'reason': 'Password reset with account unlock per KB-01',
                    'kb_sources': ['KB-01'],
                    'instructions': 'Your account has been unlocked. You can now reset your password via the self-service portal. No approval required per KB-01.',
                    'reasoning_steps': reasoning_steps
                }
            
            reasoning_steps.append("- Per KB-01: Password reset via self-service portal, no approval required")
            reasoning_steps.append("- Decision: Auto-resolve")
            
            return {
                'action': 'resolve',
                'reason': 'Password reset allowed via self-service per KB-01',
                'kb_sources': ['KB-01'],
                'instructions': 'Reset your password via the self-service portal. No approval required per KB-01.',
                'reasoning_steps': reasoning_steps
            }
        
        # VPN ACCESS
        if category == 'vpn':
            employee_type = entities.get('employee_type', 'full-time')
            reasoning_steps.append(f"- Employee type: {employee_type}")
            
            if employee_type == 'contractor':
                reasoning_steps.append("- Per KB-02: Contractors require manager approval")
                reasoning_steps.append("- Decision: Escalate to Manager")
                
                return {
                    'action': 'escalate',
                    'escalate_to': 'Manager (via access request form)',
                    'reason': 'Contractor VPN access requires manager approval per KB-02',
                    'kb_sources': ['KB-02'],
                    'instructions': 'Submit access request form with manager approval. Contractors require approval per KB-02.',
                    'reasoning_steps': reasoning_steps
                }
            else:
                reasoning_steps.append("- Per KB-02: Full-time employees have automatic VPN access")
                reasoning_steps.append("- VPN credentials expire every 90 days")
                reasoning_steps.append("- Decision: Auto-resolve (direct to renewal)")
                
                return {
                    'action': 'resolve',
                    'reason': 'VPN credential renewal for full-time employee per KB-02',
                    'kb_sources': ['KB-02'],
                    'instructions': 'Your VPN credentials have expired. Please renew them via the self-service portal. VPN access is automatic for full-time employees per KB-02.',
                    'reasoning_steps': reasoning_steps
                }
        
        # LAPTOP REPLACEMENT
        if category == 'laptop':
            laptop_age = entities.get('laptop_age')
            reasoning_steps.append(f"- Laptop age: {laptop_age if laptop_age else 'not specified'} years")
            reasoning_steps.append(f"- Hardware issue: {'Yes' if entities.get('definitely_broken') else 'Mentioned'}")
            reasoning_steps.append("- Per KB-03: Laptops eligible after 3 years OR verified hardware failure")
            reasoning_steps.append("- Note: Asset Management Policy specifies 4-year cycle (potential conflict)")
            
            # For laptops around 3-4 years, there might be a conflict
            # This should have been caught by conflict detection, but double-check
            if laptop_age and 3 <= laptop_age < 4:
                reasoning_steps.append("- ⚠️ Laptop is in 3-4 year range where policies conflict")
            
            reasoning_steps.append("- Decision: Escalate for IT approval (requires 2-week advance notice)")
            
            return {
                'action': 'escalate',
                'escalate_to': 'IT Management',
                'reason': f'Laptop replacement request (hardware failure, {laptop_age}yr old) per KB-03',
                'kb_sources': ['KB-03'],
                'instructions': 'Laptop replacement eligible per KB-03. Request must be raised at least 2 weeks in advance. IT will assess hardware failure and process approval.',
                'reasoning_steps': reasoning_steps
            }
        
        # GUEST WIFI
        if category == 'wifi':
            reasoning_steps.append("- Per KB-07: Guest WiFi can be generated by any employee")
            reasoning_steps.append("- No IT ticket required")
            reasoning_steps.append("- Decision: Auto-resolve")
            
            return {
                'action': 'resolve',
                'reason': 'Guest Wi-Fi can be self-generated per KB-07',
                'kb_sources': ['KB-07'],
                'instructions': 'Generate guest Wi-Fi credentials from the front-desk kiosk. Credentials are valid for 24 hours. No IT ticket required per KB-07.',
                'reasoning_steps': reasoning_steps
            }
        
        # SOFTWARE INSTALLATION
        if category == 'software':
            reasoning_steps.append("- Per KB-04: Non-catalog software requires IT Security review")
            reasoning_steps.append("- Review takes 3-5 business days")
            reasoning_steps.append("- Decision: Escalate to IT Security")
            
            return {
                'action': 'escalate',
                'escalate_to': 'IT Security',
                'reason': 'Non-catalog software requires security review per KB-04',
                'kb_sources': ['KB-04'],
                'instructions': 'Non-catalog software requires IT Security review per KB-04. Review takes 3-5 business days. Please provide software name, vendor, and business justification.',
                'reasoning_steps': reasoning_steps
            }
        
        # PRINTER
        if category == 'printer':
            reasoning_steps.append("- Per KB-05: First check printer queue and restart print spooler")
            reasoning_steps.append("- If issue persists, log ticket with asset tag")
            reasoning_steps.append("- Decision: Provide troubleshooting guidance")
            
            return {
                'action': 'resolve',
                'reason': 'Printer troubleshooting steps per KB-05',
                'kb_sources': ['KB-05'],
                'instructions': 'Per KB-05: First, check the printer queue and restart the print spooler. If the issue persists after these steps, log a ticket with the printer\'s asset tag for technician support.',
                'reasoning_steps': reasoning_steps
            }
        
        # MAILBOX QUOTA
        if category == 'mailbox':
            reasoning_steps.append("- Per KB-06: Default quota is 25GB")
            reasoning_steps.append("- Employees should archive old mail")
            reasoning_steps.append("- Quota increase requires manager approval (capped at 50GB)")
            reasoning_steps.append("- Decision: Provide guidance with escalation option")
            
            return {
                'action': 'resolve',
                'reason': 'Mailbox quota guidance per KB-06',
                'kb_sources': ['KB-06'],
                'instructions': 'Per KB-06: Please archive old emails to free up space (default quota is 25GB). If you need a quota increase beyond 25GB, this requires manager approval and is capped at 50GB.',
                'reasoning_steps': reasoning_steps
            }
        
        # WORK-FROM-HOME EQUIPMENT
        if category == 'wfh_equipment':
            remote_days = entities.get('remote_days_per_week', 0)
            reasoning_steps.append(f"- Remote days per week: {remote_days}")
            reasoning_steps.append("- Per KB-10: Eligibility requires 3+ days/week remote")
            
            if remote_days >= 3:
                reasoning_steps.append("- Employee is eligible for one-time home office allowance")
                reasoning_steps.append("- Requires manager sign-off and Finance processing")
                reasoning_steps.append("- Decision: Escalate to Manager then Finance")
                
                return {
                    'action': 'escalate',
                    'escalate_to': 'Manager (for sign-off) then Finance',
                    'reason': f'WFH equipment eligible ({remote_days} days/week) per KB-10',
                    'kb_sources': ['KB-10'],
                    'instructions': 'You qualify for one-time home office equipment allowance (chair, monitor) per KB-10. Requires manager sign-off and Finance processing. IT will handle shipping once approved.',
                    'reasoning_steps': reasoning_steps
                }
            else:
                reasoning_steps.append("- Employee does not meet 3+ days/week threshold")
                reasoning_steps.append("- Decision: Not eligible per policy")
                
                return {
                    'action': 'resolve',
                    'reason': 'Does not meet WFH equipment eligibility per KB-10',
                    'kb_sources': ['KB-10'],
                    'instructions': f'Per KB-10: Home office equipment allowance requires working remotely 3+ days/week. You indicated {remote_days} days/week.',
                    'reasoning_steps': reasoning_steps
                }
        
        # ADMIN ACCESS
        if category == 'admin_access':
            reasoning_steps.append("- Admin/server access request")
            reasoning_steps.append("- No specific KB policy covers this")
            
            # Check for precedent
            if existing_tickets:
                rejected_access = [t for t in existing_tickets if 'admin access' in t.get('issue_summary', '').lower() and 'rejected' in t.get('status', '').lower()]
                if rejected_access:
                    reasoning_steps.append(f"- Precedent: {rejected_access[0]['id']} rejected due to no business justification")
            
            reasoning_steps.append("- Requires business justification and manager approval")
            reasoning_steps.append("- Decision: Escalate for review")
            
            return {
                'action': 'escalate',
                'escalate_to': 'IT Security and Manager',
                'reason': 'Admin access requires justification and approval',
                'kb_sources': [],
                'instructions': 'Admin access requests require: (1) Clear business justification, (2) Manager approval, (3) IT Security review. Note: Previous similar requests (e.g., TK-1050) were rejected without proper justification.',
                'reasoning_steps': reasoning_steps,
                'precedent': 'TK-1050 (Admin access rejected - no business justification)'
            }
        
        # EXPENSE SOFTWARE
        if category == 'expense':
            reasoning_steps.append("- Per KB-08: Expense software access managed by Finance, not IT")
            reasoning_steps.append("- IT can only help with technical issues for existing accounts")
            reasoning_steps.append("- Decision: Route to Finance")
            
            return {
                'action': 'escalate',
                'escalate_to': 'Finance Department',
                'reason': 'Expense software access managed by Finance per KB-08',
                'kb_sources': ['KB-08'],
                'instructions': 'Per KB-08: Access to expense management tool is granted by Finance, not IT. IT can only assist with login/technical issues once your account exists. Please contact Finance for access.',
                'reasoning_steps': reasoning_steps
            }
        
        # DEFAULT: Escalate with policy reference
        reasoning_steps.append(f"- Default action: Escalate per {primary_policy['id']}")
        
        return {
            'action': 'escalate',
            'escalate_to': 'IT Management',
            'reason': f'Requires approval per {primary_policy["id"]}',
            'kb_sources': [primary_policy['id']],
            'instructions': primary_policy['content'],
            'reasoning_steps': reasoning_steps
        }
