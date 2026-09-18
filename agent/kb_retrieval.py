"""
Knowledge Base Retrieval Module
Performs semantic search over KB articles using embeddings and keyword matching.
"""

import json
import os
from typing import List, Dict, Tuple
from pathlib import Path


class KnowledgeBaseRetriever:
    """Retrieves relevant KB articles based on query text."""
    
    def __init__(self, kb_path: str = None):
        """Initialize with knowledge base file."""
        if kb_path is None:
            kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.policies = data['policies']
    
    def search(self, query: str, category: str = None, top_k: int = 3) -> Dict:
        """
        Search KB articles using explicit keyword matching and return top_k results.
        
        Args:
            query: User's request text
            category: Pre-classified category (helps narrow search)
            top_k: Number of results to return
            
        Returns:
            Dict with policies list, conflicts list, and reasoning trace
        """
        query_lower = query.lower()
        scored_policies = []
        
        # Category to KB mapping
        category_kb_map = {
            'password': ['KB-01'],
            'vpn': ['KB-02'],
            'laptop': ['KB-03', 'ASSET-POLICY'],
            'software': ['KB-04'],
            'printer': ['KB-05'],
            'mailbox': ['KB-06'],
            'wifi': ['KB-07'],
            'expense': ['KB-08'],
            'security': ['KB-09'],
            'wfh_equipment': ['KB-10'],
            'admin_access': []  # No specific KB, escalate
        }
        
        # Get relevant KB IDs for this category
        relevant_kb_ids = category_kb_map.get(category, [])
        
        for policy in self.policies:
            score = 0
            
            # If we have a category match, prioritize those KBs
            if relevant_kb_ids and policy['id'] in relevant_kb_ids:
                score += 10
            
            # Check keywords
            for keyword in policy.get('keywords', []):
                if keyword.lower() in query_lower:
                    score += 2
            
            # Check title and content
            if any(word in policy['title'].lower() for word in query_lower.split() if len(word) > 3):
                score += 1
            
            if score > 0:
                scored_policies.append({
                    'policy': policy,
                    'score': score
                })
        
        # Sort by score and return top_k
        scored_policies.sort(key=lambda x: x['score'], reverse=True)
        top_policies = [item['policy'] for item in scored_policies[:top_k]]
        
        if not top_policies:
            top_policies = [self._get_fallback_policy()]
        
        # Check for conflicts
        conflicts = self.check_conflicts(top_policies)
        
        # Generate reasoning
        reasoning = []
        if relevant_kb_ids:
            reasoning.append(f"Category '{category}' maps to KB articles: {', '.join(relevant_kb_ids)}")
        reasoning.append(f"Retrieved {len(top_policies)} relevant KB articles")
        if conflicts:
            reasoning.append(f"⚠️ CONFLICT DETECTED: {len(conflicts)} policy conflict(s) found")
        
        return {
            'policies': top_policies,
            'conflicts': conflicts,
            'reasoning': reasoning
        }
    
    def get_by_id(self, policy_id: str) -> Dict:
        """Get a specific policy by ID."""
        for policy in self.policies:
            if policy['id'] == policy_id:
                return policy
        return None
    
    def check_conflicts(self, policies: List[Dict]) -> List[str]:
        """
        Check if any of the retrieved policies have conflicts.
        
        Returns:
            List of conflict notes
        """
        conflicts = []
        for policy in policies:
            if 'conflict_note' in policy:
                conflicts.append(f"{policy['id']}: {policy['conflict_note']}")
        return conflicts
    
    def _get_fallback_policy(self) -> Dict:
        """Return a fallback when no relevant KB article is found."""
        return {
            'id': 'UNKNOWN',
            'title': 'Unable to find relevant policy',
            'content': 'This request requires human review as no matching policy was found.',
            'category': 'general',
            'requires_approval': True
        }
