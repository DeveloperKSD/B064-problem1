import streamlit as st
import json
from datetime import datetime
from agent.agent import SupportAgent

# Page config
st.set_page_config(
    page_title="Self-Healing Support Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = SupportAgent()

if 'ticket_history' not in st.session_state:
    st.session_state.ticket_history = []

if 'processing_log' not in st.session_state:
    st.session_state.processing_log = []

# Custom CSS
st.markdown("""
<style>
    .ticket-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        color: black;
        background-color: #f8f9fa;
        margin: 15px 0;
    }
    
    .severity-critical {
        border-left-color: #dc3545 !important;
        background-color: #f8d7da !important;
    }
    
    .severity-high {
        border-left-color: #fd7e14 !important;
        background-color: #fff3cd !important;
    }
    
    .severity-medium {
        border-left-color: #ffc107 !important;
    }
    
    .severity-low {
        border-left-color: #28a745 !important;
        background-color: #d4edda !important;
    }
    
    .analysis-box {
        padding: 15px;
        background-color: #e8f4f8;
        color: black;
        border-left: 4px solid #0066cc;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .decision-box {
        padding: 15px;
        background-color: #fff3e0;
        color: black;
        border-left: 4px solid #ff9800;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .result-box {
        padding: 15px;
        background-color: #e8f5e9;
        color: black;
        border-left: 4px solid #4caf50;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .approval-needed {
        padding: 20px;
        background-color: #fff3cd;
        color: black;
        border: 3px solid #ffc107;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .confidence-high { color: #28a745; font-weight: bold; }
    .confidence-medium { color: #ffc107; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Self-Healing Support Agent")
st.markdown("*Intelligent ticket processing for E-commerce website*")
st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "📝 Submit Ticket",
    "📂 Process Pending Tickets", 
    "📊 History & Analytics"
])

# ============================================================================
# TAB 1: SUBMIT NEW TICKET
# ============================================================================
with tab1:
    st.header("📝 Submit New Ticket")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("ticket_form", clear_on_submit=True):
            st.subheader("Ticket Details")
            
            merchant_id = st.text_input(
                "Merchant ID",
                placeholder="e.g., MERCH-12345",
                help="Enter the merchant identifier"
            )
            
            description = st.text_area(
                "Problem Description",
                placeholder="Describe the issue in detail...",
                height=150,
                help="Provide a detailed description of the problem"
            )
            
            severity = st.selectbox(
                "Severity Level",
                options=['low', 'medium', 'high', 'critical'],
                index=1,
                help="Select the severity of the issue"
            )
            
            submit_button = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)
        
        if submit_button:
            if not merchant_id or not description:
                st.error("❌ Please fill in all required fields (Merchant ID and Description)")
            else:
                # Create ticket
                ticket = {
                    'id': f"T-{hash(description) % 10000:04d}",
                    'merchant_id': merchant_id,
                    'description': description,
                    'severity': severity,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.success(f"✅ Ticket created: {ticket['id']}")
                
                # Process ticket
                with st.spinner("🔍 Analyzing ticket..."):
                    # Display ticket info
                    severity_class = f"severity-{severity}"
                    st.markdown(f"""
                    <div class="ticket-card {severity_class}">
                        <h4>📋 Ticket #{ticket['id']}</h4>
                        <p><strong>Merchant:</strong> {ticket['merchant_id']}</p>
                        <p><strong>Severity:</strong> {severity.upper()}</p>
                        <p><strong>Issue:</strong> {ticket['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # OBSERVE → REASON
                    analysis = st.session_state.agent.reason(ticket)
                    
                    st.markdown("### 🧠 REASONING ANALYSIS")
                    confidence_class = "confidence-high" if analysis['confidence'] >= 0.8 else "confidence-medium" if analysis['confidence'] >= 0.6 else "confidence-low"
                    
                    st.markdown(f"""
                    <div class="analysis-box">
                        <p><strong>Root Cause:</strong> {analysis['root_cause']}</p>
                        <p><strong>Confidence:</strong> <span class="{confidence_class}">{analysis['confidence']:.0%}</span></p>
                        <p><strong>Explanation:</strong> {analysis['reasoning']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # DECIDE
                    decision = st.session_state.agent.decide(ticket, analysis)
                    
                    st.markdown("### 💡 PROPOSED ACTION")
                    st.markdown(f"""
                    <div class="decision-box">
                        <p><strong>Action:</strong> {decision['action']}</p>
                        <p><strong>Risk Level:</strong> {decision['risk_level'].upper()}</p>
                        <p><strong>Requires Approval:</strong> {'Yes ⚠️' if decision['needs_human_approval'] else 'No ✅'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Human approval if needed
                    if decision['needs_human_approval']:
                        st.markdown("### ⚠️ HIGH RISK - HUMAN APPROVAL REQUIRED")
                        
                        # Determine reason for approval
                        approval_reason = []
                        if ticket['severity'] == 'critical':
                            approval_reason.append("Critical severity ticket")
                        if decision['confidence'] < 0.7:
                            approval_reason.append(f"Low confidence ({decision['confidence']:.0%})")
                        if decision['root_cause'] == 'platform_bug':
                            approval_reason.append("Potential platform bug")
                        
                        st.markdown(f"""
                        <div class="approval-needed">
                            <h4>🚨 Approval Required</h4>
                            <p><strong>Reason(s):</strong></p>
                            <ul>
                                {''.join([f'<li>{r}</li>' for r in approval_reason])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_approve, col_reject = st.columns(2)
                        
                        with col_approve:
                            if st.button("✅ Approve Action", key="approve", use_container_width=True):
                                # ACT
                                result = st.session_state.agent.act(ticket, decision)
                                
                                st.markdown("### ⚡ ACTION EXECUTED")
                                st.markdown(f"""
                                <div class="result-box">
                                    <p><strong>Status:</strong> {result['status']}</p>
                                    <p><strong>Action Taken:</strong> {result['action']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Add to history
                                st.session_state.ticket_history.append({
                                    'ticket': ticket,
                                    'analysis': analysis,
                                    'decision': decision,
                                    'result': result,
                                    'approved': True
                                })
                                
                                st.balloons()
                        
                        with col_reject:
                            if st.button("❌ Reject Action", key="reject", use_container_width=True):
                                st.warning("❌ Action REJECTED by human")
                                st.session_state.agent.memory.store(ticket, decision, {"status": "rejected_by_human"})
                                
                                # Add to history
                                st.session_state.ticket_history.append({
                                    'ticket': ticket,
                                    'analysis': analysis,
                                    'decision': decision,
                                    'result': {"status": "rejected_by_human"},
                                    'approved': False
                                })
                    else:
                        # ACT (auto-approved)
                        result = st.session_state.agent.act(ticket, decision)
                        
                        st.markdown("### ⚡ ACTION EXECUTED")
                        st.markdown(f"""
                        <div class="result-box">
                            <p><strong>Status:</strong> {result['status']}</p>
                            <p><strong>Action Taken:</strong> {result['action']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.ticket_history.append({
                            'ticket': ticket,
                            'analysis': analysis,
                            'decision': decision,
                            'result': result,
                            'approved': True
                        })
                        
                        st.success("✅ Ticket processed successfully!")
    
    with col2:
        st.subheader("📋 Quick Guide")
        st.info("""
        **Workflow:**
        1. 🔍 **Observe** - Agent reads ticket
        2. 🧠 **Reason** - Analyzes root cause
        3. 💡 **Decide** - Proposes action
        4. ⚡ **Act** - Executes (with approval if needed)
        
        **Severity Levels:**
        - 🔴 Critical - Immediate attention
        - 🟠 High - Urgent
        - 🟡 Medium - Standard
        - 🟢 Low - Non-urgent
        """)
        
        st.markdown("---")
        
        st.subheader("📊 Quick Stats")
        total_tickets = len(st.session_state.ticket_history)
        approved = sum(1 for t in st.session_state.ticket_history if t.get('approved', False))
        rejected = total_tickets - approved
        
        st.metric("Total Tickets", total_tickets)
        st.metric("Approved", approved)
        st.metric("Rejected", rejected)

# ============================================================================
# TAB 2: PROCESS PENDING TICKETS
# ============================================================================
with tab2:
    st.header("📂 Process Pending Tickets from File")
    
    st.info("This will load tickets from the file system using the agent's observe() method.")
    
    if st.button("🔄 Load & Process Pending Tickets", use_container_width=True):
        with st.spinner("Loading pending tickets..."):
            tickets = st.session_state.agent.observe()
            
            if not tickets:
                st.success("✅ No pending tickets in file.")
            else:
                st.success(f"Found {len(tickets)} pending ticket(s)")
                
                for idx, ticket in enumerate(tickets, 1):
                    st.markdown(f"### Ticket {idx} of {len(tickets)}")
                    
                    severity_class = f"severity-{ticket.get('severity', 'medium')}"
                    st.markdown(f"""
                    <div class="ticket-card {severity_class}">
                        <h4>📋 Ticket #{ticket['id']}</h4>
                        <p><strong>Merchant:</strong> {ticket['merchant_id']}</p>
                        <p><strong>Issue:</strong> {ticket['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Process each ticket
                    with st.expander(f"🔍 View Processing for {ticket['id']}", expanded=True):
                        # REASON
                        analysis = st.session_state.agent.reason(ticket)
                        
                        st.markdown("**🧠 REASONING:**")
                        confidence_class = "confidence-high" if analysis['confidence'] >= 0.8 else "confidence-medium" if analysis['confidence'] >= 0.6 else "confidence-low"
                        
                        st.markdown(f"""
                        <div class="analysis-box">
                            <p><strong>Root Cause:</strong> {analysis['root_cause']}</p>
                            <p><strong>Confidence:</strong> <span class="{confidence_class}">{analysis['confidence']:.0%}</span></p>
                            <p><strong>Explanation:</strong> {analysis['reasoning']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # DECIDE
                        decision = st.session_state.agent.decide(ticket, analysis)
                        
                        st.markdown("**💡 PROPOSED ACTION:**")
                        st.markdown(f"""
                        <div class="decision-box">
                            <p><strong>Action:</strong> {decision['action']}</p>
                            <p><strong>Risk Level:</strong> {decision['risk_level'].upper()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Handle approval
                        if decision['needs_human_approval']:
                            st.warning("⚠️ HIGH RISK - Requires Approval")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                approve_key = f"approve_{ticket['id']}_{idx}"
                                if st.button(f"✅ Approve", key=approve_key, use_container_width=True):
                                    result = st.session_state.agent.act(ticket, decision)
                                    st.success(f"✅ {result['status']} - {result['action']}")
                            
                            with col2:
                                reject_key = f"reject_{ticket['id']}_{idx}"
                                if st.button(f"❌ Reject", key=reject_key, use_container_width=True):
                                    st.warning("❌ Action rejected")
                                    st.session_state.agent.memory.store(ticket, decision, {"status": "rejected_by_human"})
                        else:
                            result = st.session_state.agent.act(ticket, decision)
                            st.markdown(f"""
                            <div class="result-box">
                                <p><strong>Status:</strong> {result['status']}</p>
                                <p><strong>Action:</strong> {result['action']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")

# ============================================================================
# TAB 3: HISTORY & ANALYTICS
# ============================================================================
with tab3:
    st.header("📊 Ticket History & Analytics")
    
    if not st.session_state.ticket_history:
        st.info("No tickets processed yet. Submit a ticket in the 'Submit Ticket' tab to get started.")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(st.session_state.ticket_history)
        approved = sum(1 for t in st.session_state.ticket_history if t.get('approved', False))
        rejected = total - approved
        
        # Calculate average confidence
        avg_confidence = sum(t['analysis']['confidence'] for t in st.session_state.ticket_history) / total if total > 0 else 0
        
        with col1:
            st.metric("Total Tickets", total)
        
        with col2:
            st.metric("Approved", approved, delta=f"{(approved/total*100):.0f}%" if total > 0 else "0%")
        
        with col3:
            st.metric("Rejected", rejected)
        
        with col4:
            st.metric("Avg Confidence", f"{avg_confidence:.0%}")
        
        st.markdown("---")
        
        # Ticket history
        st.subheader("📜 Ticket History")
        
        for idx, record in enumerate(reversed(st.session_state.ticket_history), 1):
            ticket = record['ticket']
            analysis = record['analysis']
            decision = record['decision']
            result = record['result']
            approved = record.get('approved', False)
            
            with st.expander(f"Ticket {len(st.session_state.ticket_history) - idx + 1}: {ticket['id']} - {ticket['merchant_id']}"):
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.markdown(f"**Description:** {ticket['description']}")
                    st.markdown(f"**Severity:** {ticket['severity'].upper()}")
                    st.markdown(f"**Root Cause:** {analysis['root_cause']}")
                    st.markdown(f"**Confidence:** {analysis['confidence']:.0%}")
                    st.markdown(f"**Action Taken:** {decision['action']}")
                    st.markdown(f"**Result:** {result['status']}")
                
                with col_right:
                    status_emoji = "✅" if approved else "❌"
                    status_text = "APPROVED" if approved else "REJECTED"
                    status_color = "#28a745" if approved else "#dc3545"
                    
                    st.markdown(f"""
                    <div style="padding: 20px; background-color: {status_color}20; border-radius: 10px; text-align: center;">
                        <h2 style="margin: 0; color: {status_color};">{status_emoji}</h2>
                        <p style="margin: 5px 0; color: {status_color}; font-weight: bold;">{status_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Download report
        st.subheader("📥 Export Data")
        
        report_data = {
            'summary': {
                'total_tickets': total,
                'approved': approved,
                'rejected': rejected,
                'average_confidence': avg_confidence
            },
            'tickets': st.session_state.ticket_history
        }
        
        st.download_button(
            label="📄 Download Full Report (JSON)",
            data=json.dumps(report_data, indent=2, default=str),
            file_name=f"ticket_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.caption("🤖 Self-Healing Support Agent | Built with Streamlit")