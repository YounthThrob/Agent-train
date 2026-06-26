import re
from core.node import BaseNode

class ParamNode(BaseNode):
    name = "param_node"

    def run(self, state):
        # 使用正则表达式提取参数
        text = state.user_input
        amount_match = re.search(r'(\d+(\.\d+)?)元', text)
        amount = float(amount_match.group(1)) if amount_match else None

        city = "上海" if "上海" in text else None
        expense_type = "酒店" if "酒店" in text else None

        state.params = {
            "amount": amount,
            "city": city,
            "expense_type": expense_type
        }

        state.add_trace(self.name, {"params": state.params})

        if amount is None:
            state.add_error("未能提取报销金额。")
        if city is None:
            state.add_error("未能提取城市信息。")
        if expense_type is None:
            state.add_error("未能提取报销类型。")

        return state