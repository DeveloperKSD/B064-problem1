"""Agent memory for learning from past issues"""
import json
import os

class Memory:
    def __init__(self, path='data/memory.json'):
        self.path = path
        self.load()
    
    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"resolved_issues": []}
    
    def get_similar_issues(self, description):
        """Retrieve similar past issues"""
        # Simple keyword match (could use embeddings)
        similar = []
        keywords = description.lower().split()[:3]
        
        for issue in self.data['resolved_issues']:
            if any(kw in issue['description'].lower() for kw in keywords):
                similar.append(issue)
        
        return similar[:3]  # Top 3
    
    def store(self, ticket, decision, result):
        """Store resolved issue"""
        self.data['resolved_issues'].append({
            'ticket_id': ticket['id'],
            'description': ticket['description'],
            'root_cause': decision.get('root_cause'),
            'action': decision['action'],
            'result': result
        })
        
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)
