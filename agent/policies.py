"""Decision policies with risk assessment"""

class PolicyEngine:
    def get_action(self, root_cause, severity, confidence):
        """Determine action based on rules"""
        
        # High-risk actions need approval
        needs_approval = (
            severity == "critical" or 
            confidence < 0.7 or
            root_cause == "platform_bug"
        )
        
        # Action mapping
        actions = {
            "merchant_config_error": "Send config fix guide to merchant",
            "platform_bug": "Escalate to engineering + apply hotfix",
            "migration_issue": "Rollback merchant to hosted mode",
            "documentation_gap": "Update docs + notify affected merchants",
            "api_misconfiguration": "Auto-fix API keys + notify merchant"
        }
        
        risk_levels = {
            "merchant_config_error": "low",
            "platform_bug": "high",
            "migration_issue": "medium",
            "documentation_gap": "low",
            "api_misconfiguration": "medium"
        }
        
        return {
            "action": actions.get(root_cause, "Escalate to human support"),
            "risk_level": risk_levels.get(root_cause, "unknown"),
            "needs_human_approval": needs_approval,
            "confidence": confidence,
            "root_cause": root_cause
        }
