def check_amount_limit(tool_input):
    """
    tool_input 示例：
    {
        "amount": 1280,
        "limit": 1500
    }
    """
    amount = float(tool_input.get("amount", 0))
    limit = float(tool_input.get("limit", 0))

    return {
        "amount": amount,
        "limit": limit,
        "passed": amount <= limit,
        "message": "金额检查通过" if amount <= limit else "金额超出限制"
    }