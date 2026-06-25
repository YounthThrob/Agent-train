from core.node import BaseNode

class RiskNode(BaseNode):
    name = "risk_node"

    def run(self, state):
        tool_input = {
            "amount": state.params.get("amount"),
            "expense_type": state.params.get("expense_type"),
            "city": state.params.get("city"),
        }

        result = self.tool_router.route("risk_check", tool_input)
        state.add_trace(self.name, {
            "tool": "risk_check",
            "tool_input": tool_input,
            "output": result
        })

        if not result["success"]:
            state.add_error(result["error"])
            return state
        
        state.risk_check_result = result["result"]

        return state