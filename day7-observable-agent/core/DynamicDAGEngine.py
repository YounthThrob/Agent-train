class DynamicDAGEngine:
    def __init__(self, node_registry, validator,repair_manager):
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
        self.validator = validator
        self.repair_manager = repair_manager

    def run(self, state):
        """
        执行DAG引擎
        """
        if not state.plan:
            state.add_error("No plan found in state. Please run the PlannerNode first.")
            return state
        
        # 1. 验证 plan 的合法性
        if self.validator:
            ok, err=self.validator.validate_plan(state.plan)
            if not ok:
                state.add_error(f"Plan validation failed: {err}")
                return state
        
        # 2. 执行节点
        for node_name in state.plan:
            print(f"\n========== 动态执行节点: {node_name} ==========")
            node = self.node_registry.get(node_name)
            if not node:
                state.add_error(f"Node {node_name} not found in registry.")
                return state
            
            # 3.验证节点输入
            if self.validator:
                ok, err=self.validator.validate_node_input(node_name, state)
                if not ok:
                    print(f"节点输入检验失败：{err}")

                    repaired = False
                    
                    if self.repair_manager and state.repair_count < state.max_repair_count:
                        state.repair_count += 1
                        repaired = self.repair_manager.repair_params(state)
                    
                    if repaired:
                        print("参数修复成功，重新执行节点输入验证。")
                        ok, err=self.validator.validate_node_input(node_name, state)
                    if not ok:
                        state.add_error(f"Node input validation failed for {node_name} after repair: {err}")
                        break         
            # 4. 执行节点
            try:
                before_errors = len(state.errors)
                output = node.run(state)

                if len(state.errors) > before_errors:
                    print(f"Node {node_name} execution failed with errors: {state.errors[-1]}")
                    break
            except Exception as e:
                state.add_error(f"Node {node_name} execution raised an exception: {str(e)}")
                break
            
            # 5. 验证节点输出
            if self.validator:
                output = self._get_node_output(node_name, state)
                ok, err=self.validator.validate_node_output(node_name, output)
                if not ok:
                    state.add_error(f"Node output validation failed for {node_name}: {err}")
                    break
        
        return state
        
    def _get_node_output(self, node_name, state):
            """
            获取节点输出
            """
            if node_name == "policy_node":
                return state.policy_result
            
            if node_name == "amount_check_node":
                return state.amount_check_result
            
            if node_name == "risk_node":
                return state.risk_result
            
            return {}
    