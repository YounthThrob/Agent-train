import random


def query_policy(tool_input):
    """
    模拟不稳定的企业制度查询接口。
    有一定概率失败，用来测试 retry / fallback。
    """
    if random.random() < 0.5:
        raise RuntimeError("制度服务暂时不可用")

    expense_type = tool_input.get("expense_type")
    city = tool_input.get("city")

    if expense_type == "酒店" and city == "上海":
        return {
            "city": "上海",
            "expense_type": "酒店",
            "limit": 1500,
            "currency": "CNY",
            "rule": "上海出差酒店报销标准上限为1500元/晚",
            "source": "primary_policy_tool"
        }

    return {
        "city": city,
        "expense_type": expense_type,
        "limit": 800,
        "currency": "CNY",
        "rule": "默认住宿报销标准上限为800元/晚",
        "source": "primary_policy_tool"
    }