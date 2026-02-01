"""Main agent loop: Observe → Reason → Decide → Act"""
import json
from .tools import TicketAnalyzer, ActionExecutor
from .memory import Memory
from .policies import PolicyEngine

class SupportAgent:
    def __init__(self):
        self.analyzer = TicketAnalyzer()
        self.executor = ActionExecutor()
        self.memory = Memory()
        self.policies = PolicyEngine()
        
    def observe(self):
        """Load tickets and system signals"""
        with open('data/tickets.json', 'r') as f:
            return json.load(f)['tickets']
    
    def reason(self, ticket):
        """Use AI to identify root cause"""
        # Get similar past issues
        context = self.memory.get_similar_issues(ticket['description'])
        
        # Analyze with Gemini
        analysis = self.analyzer.analyze(ticket, context)
        return analysis
    
    def decide(self, ticket, analysis):
        """Determine action based on policies"""
        decision = self.policies.get_action(
            root_cause=analysis['root_cause'],
            severity=ticket['severity'],
            confidence=analysis['confidence']
        )
        return decision
    
    def act(self, ticket, decision):
        """Execute or queue action"""
        if decision['needs_human_approval']:
            print(f"⏸️  Ticket #{ticket['id']}: AWAITING HUMAN APPROVAL")
            return {"status": "pending_approval", "action": decision}
        
        result = self.executor.execute(decision)
        self.memory.store(ticket, decision, result)
        return result
    
    def run(self):
        """Main agent loop"""
        tickets = self.observe()
        results = []
        
        for ticket in tickets:
            print(f"\n🔍 Processing Ticket #{ticket['id']}...")
            
            # OBSERVE → REASON → DECIDE → ACT
            analysis = self.reason(ticket)
            decision = self.decide(ticket, analysis)
            result = self.act(ticket, decision)
            
            results.append({
                'ticket_id': ticket['id'],
                'issue': ticket['description'][:50] + "...",
                'root_cause': analysis['root_cause'],
                'action': decision['action'],
                'risk_level': decision['risk_level'],
                'needs_human_approval': decision['needs_human_approval']
            })
        
        return results