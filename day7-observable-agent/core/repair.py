import re


class RepairManager:
    def repair_params(self, state):
        """
        尝试从 user_input 中重新修复参数。
        """
        text = state.user_input
        repaired = False

        # 修复 amount
        if state.params.get("amount") is None:
            amount_match = re.search(r"(\d+(\.\d+)?)\s*元", text)
            if amount_match:
                state.params["amount"] = float(amount_match.group(1))
                repaired = True

        # 修复 city
        if state.params.get("city") is None:
            if "上海" in text:
                state.params["city"] = "上海"
                repaired = True
            elif "北京" in text:
                state.params["city"] = "北京"
                repaired = True
            elif "深圳" in text:
                state.params["city"] = "深圳"
                repaired = True

        # 修复 expense_type
        if state.params.get("expense_type") is None:
            if "酒店" in text or "住宿" in text:
                state.params["expense_type"] = "酒店"
                repaired = True
            elif "餐饮" in text or "吃饭" in text:
                state.params["expense_type"] = "餐饮"
                repaired = True
            elif "交通" in text or "打车" in text:
                state.params["expense_type"] = "交通"
                repaired = True

        state.add_trace("repair_params", {
            "repaired": repaired,
            "params": state.params
        })

        return repaired