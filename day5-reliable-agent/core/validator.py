
class Validator:
    ALLOWED_NODES = {
        "param_node",
        "policy_node",
        "amount_check_node",
        "risk_node",
        "final_node",
    }

    NODE_INPUT_REQUIREMENTS = {
        "policy_node": ["expense_type", "city"],
        "amount_check_node": ["amount"],
        "risk_node": ["amount", "expense_type", "city"],
    }

    NODE_OUTPUT_REQUIREMENTS = {
        "policy_node": ["limit", "rule", "currency"],
        "amount_check_node": ["amount", "limit", "passed", "message"],
        "risk_node": ["risk_level", "risk_flags", "passed"],
    }

    def validate_plan(self, plan):
        if not isinstance(plan, list):
            return False, "plan 必须是 list"

        if not plan:
            return False, "plan 不能为空"

        for node_name in plan:
            if node_name not in self.ALLOWED_NODES:
                return False, f"非法节点: {node_name}"

        if "param_node" not in plan:
            return False, "plan 缺少 param_node"

        if "final_node" not in plan:
            return False, "plan 缺少 final_node"

        if plan[-1] != "final_node":
            return False, "final_node 必须在最后"

        return True, None

    def validate_node_input(self, node_name, state):
        required_fields = self.NODE_INPUT_REQUIREMENTS.get(node_name, [])

        for field in required_fields:
            value = state.params.get(field)

            if value is None or value == "":
                return False, f"{node_name} 缺少输入参数: {field}"

        return True, None

    def validate_node_output(self, node_name, output):
        required_fields = self.NODE_OUTPUT_REQUIREMENTS.get(node_name, [])

        if not required_fields:
            return True, None

        if not isinstance(output, dict):
            return False, f"{node_name} 输出必须是 dict"

        for field in required_fields:
            if field not in output:
                return False, f"{node_name} 输出缺少字段: {field}"

        return True, None