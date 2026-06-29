from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class AgentState:
    # 用户输入
    user_input: str
    user_id: str = "default_user"
    # 用户意图
    intent: Optional[str] = None
    # 抽取参数
    params: Dict[str, Any] = field(default_factory=dict)
    # Planner生成的执行计划
    plan: List[str] = field(default_factory=list)
    # 策略结果
    policy_result: Dict[str, Any] = field(default_factory=dict)
    # 金额检查结果
    amount_check_result: Dict[str, Any] = field(default_factory=dict)
    # 风险结果
    risk_result: Dict[str, Any] = field(default_factory=dict)
    # 任务执行结果
    final_output: Optional[str] = None
    # 记忆信息
    memory: Dict[str, Any] = field(default_factory=dict)
    # 错误信息
    errors: List[str] = field(default_factory=list)
    # 警告信息
    warnings: List[str] = field(default_factory=list)
    # 执行过程追踪信息
    trace: List[Dict[str, Any]] = field(default_factory=list)
    # 修复次数
    repair_count: int = 0
    max_repair_count: int = 3

    def add_trace(self, node_name: str, data: Dict[str, Any]):
        self.trace.append({
            "node": node_name, 
            "data": data
        })

    def add_error(self, error: str):
        self.errors.append(error)

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def clear_errors(self):
        self.errors.clear()