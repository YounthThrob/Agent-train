# 工具调用中段
        ┌──────────────┐
        │    LLM       │
        └─────┬────────┘
              ↓
     🔒 JSON Schema Guard
              ↓
      Tool Parser (strict)
              ↓
        Tool Router
              ↓
     Structured Tool Result
              ↓
        回填 LLM
# tool后段
User Question
   ↓
Thought（思考）
   ↓
Action（调用工具）
   ↓
Observation（工具结果）
   ↓
Thought（再思考）
   ↓
Action
   ↓
Observation
   ↓
Final Answer

## 给ReAct弱约束，不走工具直接输出
请输入问题（exit退出）: 1+2*3是多少

[Step 0 LLM]:
 Thought: 需要计算1+2*3，根据数学运算优先级，先乘法后加法。我先计算2乘以3等于6，然后1加6得到7。
Action: none
Action Input: none
Final Answer: 7

✅ Final Answer: 7
## 加入强约束提示词
SYSTEM_PROMPT = """
你是一个严格的ReAct Agent。

你必须遵守规则：

========================
所有计算必须使用工具 calculator
禁止你自己计算结果
========================

输出格式：

Thought: 思考
Action: calculator 或 search 或 none
Action Input: 输入内容

如果没有工具才输出：
Final Answer: 答案

========================
禁止：
- 直接算数学题
- 直接输出答案
"""
## 重新的运算结果
[Step 0 LLM]:
 Thought: 需要计算表达式 "1+2*3"。根据运算顺序，乘法优先于加法，但我不能自行计算，必须使用 calculator 工具。
Action: calculator
Action Input: 1+2*3

🔧 Tool Result: {'success': True, 'result': '7', 'error': None}

[Step 1 LLM]:
 Thought: 工具返回了计算结果 7，因此可以给出最终答案。
Final Answer: 7

✅ Final Answer: 7

# 总结
prompt.py给了模型自由，LLM会选择“更快的路径”，认为自己可以计算，因此不走工具；
而prompt_ReAct.py强制约束，所以模型必须走工具流程