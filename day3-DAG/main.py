from llm import LLM
from core.tool_router import ToolRouter
from core.state import AgentState as State
from core.dag_engine import DAGEngine

from nodes.intent_node import IntentNode
from nodes.param_node  import ParamNode
from nodes.policy_node import PolicyNode
from nodes.amount_check_node import AmountCheckNode
from nodes.risk_node import RiskNode
from nodes.final_node import FinalNode
from nodes.planner_node import PlannerNode


def build_agent():
    """
    Build and return an agent for the DAG.
    """
    # Implementation of the agent building logic goes here
    llm = LLM()  # Initialize your LLM here
    tool_router = ToolRouter()  # Initialize your tool router here

    # 1. Planner 单独执行
    planner_node = PlannerNode(llm, tool_router)

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
    engine = DAGEngine(node_registry)
    return engine,planner_node

def run_agent(user_input):
    """
    Run the agent with the given user input.
    """
    # state = State(user_input)
    # engine = build_agent()

    # result_state = engine.run(state)
    # print("\n========== 最终结果 ==========")
    # if result_state.errors:
    #     print("执行过程中出现错误：")
    #     for error in result_state.errors:
    #         print(f"- {error}")
    # else:
    #     print(result_state.final_output)

    # print("\n========== 执行轨迹 ==========")
    # for trace in result_state.trace:
    #     print(trace)

    # 1. 构建Agent
    engine, planner_node = build_agent()

    # 2. 初始化状态
    state = State(user_input=user_input)

    # 3. 执行Planner节点，生成执行计划
    print("\n========== Planner 生成执行计划 ==========")
    state = planner_node.run(state)

    if state.errors:
        print("Planner执行过程中出现错误：")
        for error in state.errors:
            print(f"- {error}")
        return
    
    print(f"生成的执行计划: {state.plan}")

    # 4. 执行DAG引擎
    print("\n========== 执行Dynamic DAG引擎 ==========")
    result_state = engine.run(state)

    # 5. 输出最终结果
    print("\n========== 最终结果 ==========")
    if result_state.errors:
        print("执行过程中出现错误：")
        for error in result_state.errors:
            print(f"- {error}")
    else:
        print(result_state.final_output)

    print("\n========== 执行轨迹 ==========")
    for trace in result_state.trace:
        print(trace)

        
if __name__ == "__main__":
    while True:
        user_input = input("\n请输入问题（exit退出）")

        if user_input.lower() == "exit":
            break
        
        run_agent(user_input)
