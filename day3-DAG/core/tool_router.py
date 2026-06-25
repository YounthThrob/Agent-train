from tools.amount_tool import check_amount_limit
from tools.policy_tool import query_policy
from tools.risk_tool import check_risk

class ToolRouter:
    def __init__(self):
        self.tools = {
            "amount_tool": check_amount_limit,
            "policy_tool": query_policy,
            "risk_tool": check_risk
        }

    def route(self, tool_name, tool_input):
        if tool_name not in self.tools:
            return {
                "success": False,
                "result": None,
                "error": f"Tool '{tool_name}' not found."
            }
        try:
            result = self.tools[tool_name](tool_input)
            return {
                "success": True,
                "result": result,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }