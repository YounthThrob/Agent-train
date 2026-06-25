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