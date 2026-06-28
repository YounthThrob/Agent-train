import json
from core.node import BaseNode
import prompt


class LLMPlannerNode(BaseNode):
    name = "llm_planner_node"

    ALLOWED_NODES = {
        "param_node",
        "policy_node",
        "amount_check_node",
        "risk_node",
        "final_node",
    }

    def run(self, state):
        prompt = f"""
你是一个企业报销 Agent 的任务规划器。

请根据用户输入，选择需要执行的节点。

可用节点如下：
1. param_node：抽取金额、城市、报销类型等参数
2. policy_node：查询报销制度、城市标准、类型标准
3. amount_check_node：检查金额是否超过制度限制
4. risk_node：检查风险、合规问题
5. final_node：生成最终回复

规则：
- final_node 必须放在最后
- param_node 通常应该放在最前
- 如果涉及制度、规则、标准，加入 policy_node
- 如果涉及金额、额度、是否超标，加入 amount_check_node
- 如果涉及风险、合规、异常，加入 risk_node
- 只能输出 JSON，不要解释

输出格式：
{{
  "plan": ["param_node", "policy_node", "final_node"]
}}

用户输入：
{state.user_input}
"""
        response = self.llm.chat([
            {"role": "user", "content": prompt}
        ])

        content = response["content"]

        try:
            data = json.loads(content)
            plan = data.get("plan", [])
        except Exception:
            state.add_error(f"Planner 输出不是合法 JSON: {content}")
            return state

        # 校验 plan
        if not isinstance(plan, list):
            state.add_error("Planner 输出 plan 不是 list")
            return state

        for node_name in plan:
            if node_name not in self.ALLOWED_NODES:
                state.add_error(f"Planner 输出非法节点: {node_name}")
                return state

        if not plan:
            state.add_error("Planner 输出空计划")
            return state

        if plan[-1] != "final_node":
            plan.append("final_node")

        if "param_node" not in plan:
            plan.insert(0, "param_node")

        state.plan = plan

        state.add_trace(self.name, {
            "plan": state.plan,
            "raw": content
        })

        return state