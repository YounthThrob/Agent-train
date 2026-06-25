def check_risk(tool_input):
    """
    简化版配置
    """
    amount = float(tool_input.get("amount", 0))
    expense_type = tool_input.get("expense_type", "")
    city = tool_input.get("city", "")

    risk_flags =[]
    # 简单的风险检查逻辑
    if amount >5000:
        risk_flags.append("金额过大，可能存在风险")
    
    if not expense_type:
        risk_flags.append("未提供报销类型，可能存在风险")

    if not city:
        risk_flags.append("未提供城市信息，可能存在风险")

    return {
        "risk_level": "高" if risk_flags else "低",
        "risk_flags": risk_flags,
        "passed": len(risk_flags) == 0
    }