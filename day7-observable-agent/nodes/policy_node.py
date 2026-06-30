from core.node import BaseNode

class PolicyNode(BaseNode):
    name = "policy_node"

    def run(self, state):
        tool_input = {
            "expense_type": state.params.get("expense_type"),
            "city": state.params.get("city"),
        }
        
        result = self.tool_router.route("query_policy", tool_input)
        
        # 记录工具调用指标
        state.tool_metrics.append({
            "trace_id": state.trace_id,
            "node": self.name,
            "tool": "query_policy",
            "success": result["success"],
            "used_fallback": result.get("used_fallback"),
            "retry_count": result.get("retry_count"),
            "latency": result.get("metadata", {}).get("latency"),
            "error": result.get("error")
        })
        state.add_trace(self.name, {
            "tool": "query_policy",
            "tool_input": tool_input, 
            "tool_result": result
        })

        if not result["success"]:
            state.add_error(result["error"])
            return state
        
        state.policy_result = result["result"]

        return state

