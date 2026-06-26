# DAY3 练习任务——DAG
## 以 企业报销审核Agent 为例
### State: 状态对象
DAG中不能靠散装变量传递数据，必须有统一的转台
    State = 当前请求执行过程中的共享数据
例如：
    用户原始输入
    意图
    参数
    制度查询结果
    金额检查结果
    风险检查结果
    最终输出
    错误信息
### Node：节点
每一个节点复杂一件事
例如：
    IntentNode：识别意图
    ParamNode：抽取参数
    PolicyNode：查询制度
    AmountCheckNode：检查金额
    RiskNode：检查风险
    FinalNode：生成最终回答

## 动态的DAG
前面的流程就是固定死的，下载是做升级
用户输入
  ↓
Planner 生成计划
  ↓
DAG Engine 根据 plan 执行指定节点
  ↓
节点结果写入 State
  ↓
FinalNode 输出结果
### 架构图
用户输入
  ↓
PlannerNode
  ↓
生成执行计划 JSON
  ↓
{
  "plan": [
    "param_node",
    "policy_node",
    "amount_check_node",
    "risk_node",
    "final_node"
  ]
}
  ↓
DynamicDAGEngine
  ↓
按 plan 找到对应 node
  ↓
逐个执行节点
  ↓
State 汇总结果
  ↓
FinalNode 输出

### 测试结果
请输入问题（exit退出）帮我检查一笔上海出差酒店报销，金额1280元，看看是否符合公司制度

========== Planner 生成执行计划 ==========
生成的执行计划: ['param_node', 'policy_node', 'amount_check_node', 'risk_node', 'final_node']

========== 执行Dynamic DAG引擎 ==========

========== 动态执行节点: param_node ==========

========== 动态执行节点: policy_node ==========

========== 动态执行节点: amount_check_node ==========

========== 动态执行节点: risk_node ==========

========== 动态执行节点: final_node ==========

========== 最终结果 ==========

报销审核结果：报销申请不通过

关键信息：
- 报销类型：酒店
- 报销金额：1280.0元
- 城市：上海

制度规则：
- None

风险检查：
- 风险等级 低
- 风险项：[]



========== 执行轨迹 ==========
{'node': 'PlannerNode', 'data': {'plan': ['param_node', 'policy_node', 'amount_check_node', 'risk_node', 'final_node']}}
{'node': 'param_node', 'data': {'params': {'amount': 1280.0, 'city': '上海', 'expense_type': '酒店'}}}
{'node': 'policy_node', 'data': {'tool': 'query_policy', 'tool_input': {'expense_type': '酒店', 'city': '上海'}, 'tool_result': {'success': True, 'result': {'city': '上海', 'expense_type': '酒店', 'limit': 800, 'currency': 'CNY', 'policy': '默认住宿报销上限为800元/晚'}, 'error': None}}}
{'node': 'amount_check_node', 'data': {'tool': 'check_amount_limit', 'tool_input': {'amount': 1280.0, 'limit': 800}, 'output': {'success': True, 'result': {'amount': 1280.0, 'limit': 800.0, 'passed': False, 'message': '金额超出限制'}, 'error': None}}}
{'node': 'risk_node', 'data': {'tool': 'check_risk', 'tool_input': {'amount': 1280.0, 'expense_type': '酒店', 'city': '上海'}, 'tool_result': {'success': True, 'result': {'risk_level': '低', 'risk_flags': [], 'passed': True}, 'error': None}}}
{'node': 'final_node', 'data': {'final_output': '\n报销审核结果：报销申请不通过\n\n关键信息：\n- 报销类型：酒店\n- 报销金额：1280.0元\n- 城市：上海\n\n制度规则：\n- None\n\n风险检查：\n- 风险等级 低\n- 风险项：[]\n\n'}}

请输入问题（exit退出）上海酒店报销标准是多少？

========== Planner 生成执行计划 ==========
生成的执行计划: ['param_node', 'policy_node', 'final_node']

========== 执行Dynamic DAG引擎 ==========

========== 动态执行节点: param_node ==========
Errors encountered in node 'param_node': ['未能提取报销金额。']

========== 最终结果 ==========
执行过程中出现错误：
- 未能提取报销金额。

========== 执行轨迹 ==========
{'node': 'PlannerNode', 'data': {'plan': ['param_node', 'policy_node', 'final_node']}}
{'node': 'param_node', 'data': {'params': {'amount': None, 'city': '上海', 'expense_type': '酒店'}}}

请输入问题（exit退出）上海酒店报销标准是多少？

========== Planner 生成执行计划 ==========
生成的执行计划: ['param_node', 'policy_node', 'final_node']

========== 执行Dynamic DAG引擎 ==========

========== 动态执行节点: param_node ==========
Errors encountered in node 'param_node': ['未能提取报销金额。']

========== 最终结果 ==========
执行过程中出现错误：
- 未能提取报销金额。

========== 执行轨迹 ==========
{'node': 'PlannerNode', 'data': {'plan': ['param_node', 'policy_node', 'final_node']}}
{'node': 'param_node', 'data': {'params': {'amount': None, 'city': '上海', 'expense_type': '酒店'}}}