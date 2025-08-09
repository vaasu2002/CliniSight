"""
    [CLASS] RulesEngine

    This class evaluates decision rules in priority order and returns the first matching decision.
"""
class RulesEngine:
    def __init__(self, rules):
        self.rules = sorted(rules, key=lambda x: x["priority"])
    
    """
    [METHOD] evaluate
    [PARAMS] context: dict - The context to evaluate the rules against
    [RETURN] dict - The first matching decision

    This method evaluates decision rules in priority order and returns the first matching decision.
    """
    def evaluate(self, context):
        for rule in self.rules:
            if self._evaluate_condition(rule["condition"], context):
                return {
                    "decision": rule["decision"],
                    "reasoning": [rule["reasoning"]],
                    "rule_name": rule["name"]
                }
        
        # Default fallback
        return {
            "decision": "use_cache",
            "reasoning": ["No specific rules matched, using default cache strategy"],
            "rule_name": "default"
        }
    
    """
    [METHOD] _evaluate_condition

    This method evaluates a condition against a context.
    """
    def _evaluate_condition(self, condition, context):
        """Simple condition evaluator - in production, use a proper expression evaluator"""
        try:
            # This is a simplified evaluator - in production you'd want something more robust
            return eval(condition, {"__builtins__": {}}, context)
        except:
            return False 