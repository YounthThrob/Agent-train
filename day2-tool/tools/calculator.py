def calculator(expression:str) -> str:
    """
    计算器工具
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Invalid expression"
    
