from core.node import BaseNode

class PlannerNode(BaseNode):    
    name = "PlannerNode"

    def run(self, state):
        text = state.user_input

        plan = []

        # 参数抽取几乎总需要
        plan.append("param_node")

        # 如果用户问制度、标准、规则，需要查制度
        if any(keyword in text for keyword in ["制度", "标准", "规则"]):
            plan.append("policy_node")
        
        # 如果用户包含金额、额度，需要查金额
        if "元" in text or "金额" in text:
            plan.append("amount_check_node")

        # 如果用户明确说检查风险、合规、是否符合只读、则做风险检查
        if any(keyword in text for keyword in ["风险", "合规", "是否符合", "检查"] ):
            plan.append("risk_node")

        # 最后一定需要输出
        plan.append("final_node")

        state.plan = plan

        state.add_trace(self.name,{
            "plan": state.plan
        })

        return state