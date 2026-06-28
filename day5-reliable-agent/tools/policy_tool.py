def query_policy(tool_input):
    """
    模拟查询企业报销制度
    tool_input:{
        "expense_type": "交通费",
        "city": "北京"
    }
    """
    expense_type = tool_input.get("expense_type")
    city = tool_input.get("city")

    # 模拟企业报销制度
    if expense_type == "酒店" and city == "上海":
        return {
            "city": "上海",
            "expense_type": "酒店",
            "limit": 1500,
            "currency": "CNY",
            "policy": "酒店住宿费用报销上限为1500元/晚"
            }
    return {
        "city": city,
        "expense_type": expense_type,
        "limit": 800,
        "currency": "CNY",
        "policy": "默认住宿报销上限为800元/晚"
    }