from core.node import BaseNode

class AmountCheckNode(BaseNode):
    name = "amount_check_node"

    def run(self, state):
        tool_input = {
            "amount": state.params.get("amount"),
            "limit": state.policy_result.get("limit"),
        }

        result = self.tool_router.route("check_amount_limit", tool_input)
        
        state.tool_metrics.append({
            "trace_id": state.trace_id,
            "node": self.name,
            "tool": "check_amount_limit",
            "success": result["success"],
            "used_fallback": result.get("used_fallback"),
            "retry_count": result.get("retry_count"),
            "latency": result.get("metadata", {}).get("latency"),
            "error": result.get("error")
        })

        state.add_trace(self.name, {
            "tool": "check_amount_limit",
            "tool_input": tool_input,
            "output": result
        })

        if not result["success"]:
            state.add_error(result["error"])
            return state
        
        state.amount_check_result = result["result"]

        return state