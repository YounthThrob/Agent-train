import re
from core.node import BaseNode

class ParamNode(BaseNode):
    name = "param_node"

    def run(self, state):
        # 使用正则表达式提取参数
        text = state.user_input
        amount_match = re.search(r'(\d+(\.\d+)?)元', text)
        amount = float(amount_match.group(1)) if amount_match else None

        city = None
        if "上海" in text:
            city = "上海"
        elif "北京" in text:
            city = "北京"
        elif "深圳" in text:
            city = "深圳"

        expense_type = None
        if "酒店" in text or "住宿" in text:
            expense_type = "酒店"
        elif "餐饮" in text or "吃饭" in text:
            expense_type = "餐饮"
        elif "交通" in text or "打车" in text:
            expense_type = "交通"

        # Day6：使用长期记忆补全缺失参数
        preferences = state.memory.get("preferences", {})

        if city is None and preferences.get("last_city"):
            city = preferences["last_city"]
            state.add_warning(f"城市参数缺失，已根据记忆补全为：{city}")

        if expense_type is None and preferences.get("last_expense_type"):
            expense_type = preferences["last_expense_type"]
            state.add_warning(f"报销类型缺失，已根据记忆补全为：{expense_type}")

        state.params = {
            "amount": amount,
            "city": city,
            "expense_type": expense_type
        }

        state.add_trace(self.name, {
            "params": state.params,
            "memory_used": preferences
        })

        if amount is None:
            state.add_error("缺少金额参数")

        if city is None:
            state.add_error("缺少城市参数")

        if expense_type is None:
            state.add_error("缺少报销类型参数")

        return state

        return state