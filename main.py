import json
from agent.agent import SupportAgent

def get_ticket_from_user():
    print("\n" + "="*60)
    print("📝 NEW TICKET SUBMISSION")
    print("="*60)
    
    merchant_id = input("Merchant ID: ").strip()
    description = input("Problem Description: ").strip()
    severity = input("Severity (critical/high/medium/low): ").strip().lower()
    
    if severity not in ['critical', 'high', 'medium', 'low']:
        severity = 'medium'
    
    return {
        'id': f"T-{hash(description) % 10000:04d}",
        'merchant_id': merchant_id,
        'description': description,
        'severity': severity
    }

def main():
    print("🤖 Self-Healing Support Agent Started")
    print("=" * 60)
    
    agent = SupportAgent()
    
    while True:
        print("\n" + "="*60)
        print("OPTIONS:")
        print("1. Submit new ticket (manual input)")
        print("2. Process pending tickets from file")
        print("3. Exit")
        print("="*60)
        
        choice = input("\nChoose option (1/2/3): ").strip()
        
        if choice == '3':
            break
        
        tickets = []
        
        if choice == '1':
            # Get live human input
            ticket = get_ticket_from_user()
            tickets = [ticket]
        elif choice == '2':
            # Load from file
            tickets = agent.observe()
            if not tickets:
                print("\n✅ No pending tickets in file.")
                continue
        else:
            print("❌ Invalid option")
            continue
        
        # Process tickets
        for ticket in tickets:
            print(f"\n🔍 Analyzing Ticket #{ticket['id']}...")
            print(f"   Merchant: {ticket['merchant_id']}")
            print(f"   Issue: {ticket['description']}")
            
            # OBSERVE → REASON
            analysis = agent.reason(ticket)
            print(f"\n🧠 REASONING:")
            print(f"   Root Cause: {analysis['root_cause']}")
            print(f"   Confidence: {analysis['confidence']:.2f}")
            print(f"   Explanation: {analysis['reasoning']}")
            
            # DECIDE
            decision = agent.decide(ticket, analysis)
            print(f"\n💡 PROPOSED ACTION:")
            print(f"   Action: {decision['action']}")
            print(f"   Risk Level: {decision['risk_level']}")
            
            # Human in the loop for high-risk
            if decision['needs_human_approval']:
                print(f"\n⚠️  HIGH RISK - HUMAN APPROVAL REQUIRED")
                print(f"   Reason: ", end="")
                if ticket['severity'] == 'critical':
                    print("Critical severity ticket")
                elif decision['confidence'] < 0.7:
                    print(f"Low confidence ({decision['confidence']:.2f})")
                elif decision['root_cause'] == 'platform_bug':
                    print("Potential platform bug")
                
                approval = input("\n   Approve this action? (yes/no): ").lower()
                
                if approval != 'yes':
                    print("   ❌ Action REJECTED by human")
                    agent.memory.store(ticket, decision, {"status": "rejected_by_human"})
                    continue
                else:
                    print("   ✅ Action APPROVED by human")
            
            # ACT
            print(f"\n⚡ EXECUTING ACTION...")
            result = agent.act(ticket, decision)
            print(f"   ✅ Status: {result['status']}")
            print(f"   ✅ Action taken: {result['action']}")
    
    print("\n🛑 Agent stopped.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Agent stopped by user (Ctrl+C)")