from llm import LLM
from core.tool_router import ToolRouter
from core.state import AgentState as State
from core.dag_engine import DAGEngine
from core.repair import RepairManager
from core.validator import Validator
from core.DynamicDAGEngine import DynamicDAGEngine
from core.memory_store import JSONMemoryStore
from core.memory import MemoryManager
from core.logger import get_logger
from core.execution_report import ExecutionReport

from nodes.intent_node import IntentNode
from nodes.param_node  import ParamNode
from nodes.policy_node import PolicyNode
from nodes.amount_check_node import AmountCheckNode
from nodes.risk_node import RiskNode
from nodes.final_node import FinalNode
from nodes.planner_node import PlannerNode
from nodes.llm_planner_node import LLMPlannerNode

logger = get_logger(__name__)

def build_agent():
    """
    Build and return an agent for the DAG.
    """
    # Implementation of the agent building logic goes here
    llm = LLM()  # Initialize your LLM here
    tool_router = ToolRouter()  # Initialize your tool router here
    memory_store = JSONMemoryStore("data/store.json")  # Initialize your memory store here
    memory_manager = MemoryManager(memory_store)  # Initialize your memory manager here
    
    # 1. Planner 单独执行
    planner_node = LLMPlannerNode(llm, tool_router)

    # 2. 注册节点
    node_registry = {
        "param_node": ParamNode(llm=llm, tool_router=tool_router),
        "policy_node": PolicyNode(llm=llm, tool_router=tool_router),
        "amount_check_node": AmountCheckNode(llm=llm, tool_router=tool_router),
        "risk_node": RiskNode(llm=llm, tool_router=tool_router),
        "final_node": FinalNode(llm=llm, tool_router=tool_router),
    }

    # nodes = [
    #     IntentNode(llm, tool_router),
    #     ParamNode(llm, tool_router),
    #     PolicyNode(llm, tool_router),
    #     AmountCheckNode(llm, tool_router),
    #     RiskNode(llm, tool_router),
    #     FinalNode(llm, tool_router)
    # ]

    # return DAGEngine(nodes)  # Return the DAG engine with the nodes
    validator = Validator()
    repair_manager = RepairManager()
    engine = DynamicDAGEngine(node_registry, validator, repair_manager)
    return engine,planner_node,memory_manager

def run_agent(user_input: str, user_id: str = "default_user"):
    engine,planner_node, memory_manager = build_agent()

    state = State(
        user_input=user_input,
        user_id=user_id
    )

    logger.info(f"[{state.trace_id}] request start | user_id={user_id}")
    # 1. 执行前加载记忆
    state = memory_manager.load(state)

    print("\n========== Planner 生成执行计划 ==========")
    state = planner_node.run(state)

    print("执行计划:", state.plan)

    if state.errors:
        logger.error(f"[{state.trace_id}] planner failed | errors={state.errors}")
        for err in state.errors:
            print("-", err)

        # 即使失败，也可以保存历史
        memory_manager.save(state)
        state.finish()
        ExecutionReport.print_report(state)
        return

    print("\n========== Dynamic DAG 开始执行 ==========")
    result_state = engine.run(state)

    # 2. 执行后保存记忆
    result_state = memory_manager.save(result_state)
    logger.info(
        f"[{result_state.trace_id}] request finish | "
        f"success={len(result_state.errors) == 0} | "
        f"latency={result_state.total_latency()}s"
    )

    print("\n========== 最终结果 ==========")

    if result_state.errors:
        print("执行失败：")
        for err in result_state.errors:
            print("-", err)
    else:
        print(result_state.final_output)

    ExecutionReport.print_report(result_state)

if __name__ == "__main__":
    while True:
        user_input = input("\n请输入问题（exit退出）: ")

        if user_input.lower() == "exit":
            break

        run_agent(user_input, user_id="u001")