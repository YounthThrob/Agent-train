from core.node import BaseNode

class PolicyNode(BaseNode):
    name = "policy_node"

    def run(self, state):
        tool_input = {
            "expense_type": state.params.get("expense_type"),
            "city": state.params.get("city"),
        }
        
        result = self.tool_router.route("query_policy", tool_input)

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

