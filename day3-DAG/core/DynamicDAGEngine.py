class DynamicDAGEngine:
    def __init__(self, node_registry):
        """
        node_registry 示例：
        {
            "param_node": ParamNode(...),
            "policy_node": PolicyNode(...),
            "amount_check_node": AmountCheckNode(...),
            "risk_node": RiskNode(...),
            "final_node": FinalNode(...)
        }
        """
        self.node_registry = node_registry

    def run(self, state):
        """
        执行DAG引擎
        """
        if not state.plan:
            state.add_error("No plan found in state. Please run the PlannerNode first.")
            return state
        
        for node_name in state.plan:
            print(f"\n========== 动态执行节点: {node_name} ==========")

            node = self.node_registry.get(node_name)

            if node is None:
                state.add_error(f"Node '{node_name}' not found in registry.")
                break

            try:
                state = node.run(state)
            except Exception as e:
                state.add_error(f"Error executing node '{node_name}': {str(e)}")
                break

            if state.errors:
                print(f"Errors encountered in node '{node_name}': {state.errors}")
                break
        
        return state
    