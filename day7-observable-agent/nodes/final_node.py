from core.node import BaseNode

class FinalNode(BaseNode):
    name = "final_node"

    def run(self, state):
        amount_passed = state.amount_check_result.get("passed")
        risk_result = state.risk_result
        risk_passed = risk_result.get("passed")
        if amount_passed and risk_passed:
            conclusion = "报销申请通过"
        else:
            conclusion = "报销申请不通过"
        state.final_output = f"""
报销审核结果：{conclusion}

关键信息：
- 报销类型：{state.params.get("expense_type")}
- 报销金额：{state.params.get("amount")}元
- 城市：{state.params.get("city")}

制度规则：
- {state.policy_result.get("rule")}

风险检查：
- 风险等级：{risk_result.get("risk_level")}
- 风险项：{risk_result.get("risk_flags")}

"""
        state.add_trace(self.name, {
            "final_output": state.final_output
        })

        return state
