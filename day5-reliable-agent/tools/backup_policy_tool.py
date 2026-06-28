def query_policy_backup_policy(tool_input):
    """
    备用制度查询工具
    模拟从本地缓存或备用知识库中查询
    """
    city = tool_input.get("city")
    expense_type = tool_input.get("expense_type")

    return {
        "city": city,
        "expense_type": expense_type,
        "limit": 1200,
        "currency": "CNY",
        "rule": f"备用制度库：{city}{expense_type}报销标准暂按1200元处理",
        "source": "backup_policy_tool"
    }
