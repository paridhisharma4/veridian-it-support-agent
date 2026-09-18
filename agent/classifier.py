"""
Intent Classification Module
Classifies user requests into categories and extracts key entities.
Uses explicit keyword matching - no LLM needed for this step.
"""

import re
from typing import Dict, List, Tuple


class IntentClassifier:
    """Classifies IT support requests into categories."""
    
    # Category patterns with keywords
    CATEGORIES = {
        'password': ['password', 'reset', 'locked out', 'login', 'authentication', 'account locked', 'sign in', 'unlock'],
        'vpn': ['vpn', 'remote access', 'credentials expired', 'virtual private network'],
        'laptop': ['laptop', 'computer', 'machine', 'device', 'hardware failure', "won't turn on", 'dead', 'flickering', 'screen'],
        'software': ['software', 'install', 'application', 'tool', 'program', 'extension', 'browser extension'],
        'printer': ['printer', 'print', 'paper jam', 'printing', 'print spooler', 'print queue'],
        'mailbox': ['mailbox', 'email', 'quota', 'storage', 'full', 'archive', 'can\'t send'],
        'wifi': ['guest', 'wifi', 'wi-fi', 'visitor', 'access'],
        'security': ['phishing', 'malware', 'security', 'suspicious email', 'unauthorized access', 'hack', 'breach', 'forward'],
        'wfh_equipment': ['work from home', 'wfh', 'remote', 'home office', 'monitor', 'chair', 'equipment'],
        'admin_access': ['access', 'permission', 'admin', 'server', 'database', 'reporting', 'finance reporting'],
        'expense': ['expense', 'finance tool', 'expense management', 'expense tool'],
        'unclear': ['not working', 'help', 'issue', 'problem']
    }
    
    def classify(self, request_text: str) -> Dict:
        """
        Classify the intent of the request using explicit keyword matching.
        
        Args:
            request_text: User's request
            
        Returns:
            Dict with category, confidence, extracted entities, and reasoning trace
        """
        request_lower = request_text.lower()
        
        # Score each category
        scores = {}
        matches = {}
        for category, keywords in self.CATEGORIES.items():
            matched = [kw for kw in keywords if kw in request_lower]
            if matched:
                scores[category] = len(matched)
                matches[category] = matched
        
        # Get top category
        if not scores:
            return {
                'category': 'unclear',
                'confidence': 0.0,
                'needs_clarification': True,
                'entities': {},
                'reasoning': 'No keywords matched any known issue category'
            }
        
        top_category = max(scores.items(), key=lambda x: x[1])
        category_name = top_category[0]
        confidence = min(top_category[1] / 3, 1.0)  # Normalize
        
        # Extract entities
        entities = self._extract_entities(request_text, category_name)
        
        # Determine if clarification needed
        needs_clarification = self._needs_clarification(category_name, entities, confidence)
        
        reasoning = f"Matched keywords: {matches[category_name]}. Confidence: {confidence:.2f}"
        
        return {
            'category': category_name,
            'confidence': confidence,
            'needs_clarification': needs_clarification,
            'entities': entities,
            'reasoning': reasoning,
            'matched_keywords': matches[category_name]
        }
    
    def _needs_clarification(self, category: str, entities: Dict, confidence: float) -> bool:
        """Determine if clarification is needed."""
        # Always need clarification for unclear category
        if category == 'unclear':
            return True
        
        # Low confidence needs clarification
        if confidence < 0.5:
            return True
        
        # VPN requests need employee type
        if category == 'vpn' and 'employee_type' not in entities:
            return True
        
        # Laptop requests need age for replacement eligibility
        if category == 'laptop' and 'laptop_age' not in entities and 'definitely_broken' not in entities:
            return True
        
        # WFH equipment needs days per week
        if category == 'wfh_equipment' and 'remote_days_per_week' not in entities:
            return True
        
        return False
    
    def _extract_entities(self, text: str, category: str) -> Dict:
        """Extract relevant entities from the request."""
        entities = {}
        text_lower = text.lower()
        
        # Extract laptop age
        age_patterns = [
            r'(\d+(?:\.\d+)?)\s*years?\s*(?:old|now)?',
            r'about\s*(\d+(?:\.\d+)?)\s*years?',
            r'had it\s*(?:about\s*)?(\d+(?:\.\d+)?)\s*years?'
        ]
        for pattern in age_patterns:
            match = re.search(pattern, text_lower)
            if match:
                entities['laptop_age'] = float(match.group(1))
                break
        
        # Check if laptop is definitely broken (even without age)
        if any(word in text_lower for word in ["won't turn on", 'dead', 'completely dead', "doesn't work"]):
            entities['definitely_broken'] = True
        
        # Extract contractor mention
        if 'contractor' in text_lower or 'contracting' in text_lower:
            entities['employee_type'] = 'contractor'
        else:
            entities['employee_type'] = 'full-time'
        
        # Extract remote work days
        remote_patterns = [r'(\d+)\s*days?\s*(?:a\s*)?week', r'(\d+)\s*days?/week']
        for pattern in remote_patterns:
            match = re.search(pattern, text_lower)
            if match:
                entities['remote_days_per_week'] = int(match.group(1))
                break
        
        # Detect security violation (forwarding phishing)
        if 'forward' in text_lower and ('phishing' in text_lower or 'suspicious' in text_lower):
            entities['security_violation'] = 'forwarding_phishing_email'
        
        # Extract urgency
        if 'urgent' in text_lower or 'immediately' in text_lower or 'asap' in text_lower:
            entities['urgency'] = 'high'
        
        # Detect locked out status
        failed_pattern = r'(\d+)\s*(?:failed\s*)?(?:attempts?|times)'
        match = re.search(failed_pattern, text_lower)
        if match:
            attempts = int(match.group(1))
            if attempts >= 5:
                entities['locked_out'] = True
                entities['failed_attempts'] = attempts
        
        return entities
    
    def generate_clarification_questions(self, category: str, entities: Dict) -> List[str]:
        """Generate follow-up questions based on missing information."""
        questions = []
        
        if category == 'unclear':
            questions.append("Could you please describe what specific issue you're experiencing? For example:")
            questions.append("- Password reset or account locked out?")
            questions.append("- VPN access problem?")
            questions.append("- Laptop or hardware issue?")
            questions.append("- Software installation request?")
            questions.append("- Email or mailbox problem?")
            questions.append("- Something else?")
            return questions
        
        if category == 'vpn' and 'employee_type' not in entities:
            questions.append("Are you a full-time employee or a contractor? (VPN access for contractors requires manager approval)")
        
        if category == 'laptop' and 'laptop_age' not in entities and 'definitely_broken' not in entities:
            questions.append("How old is your current laptop? This helps determine replacement eligibility.")
        
        if category == 'wfh_equipment' and 'remote_days_per_week' not in entities:
            questions.append("How many days per week are you working from home? (Eligibility requires 3+ days/week)")
        
        if category == 'software':
            questions.append("Is this software in the approved catalog, or is it a new tool that needs security review?")
        
        if category == 'admin_access':
            questions.append("What is the business justification for this access request? Please provide specific details.")
        
        return questions
