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


def build_agent():
    """
    Build and return an agent for the DAG.
    """
    # Implementation of the agent building logic goes here
    llm = LLM()  # Initialize your LLM here
    tool_router = ToolRouter()  # Initialize your tool router here

    nodes = [
        IntentNode(llm, tool_router),
        ParamNode(llm, tool_router),
        PolicyNode(llm, tool_router),
        AmountCheckNode(llm, tool_router),
        RiskNode(llm, tool_router),
        FinalNode(llm, tool_router)
    ]

    return DAGEngine(nodes)  # Return the DAG engine with the nodes

def run_agent(user_input):
    """
    Run the agent with the given user input.
    """
    state = State(user_input)
    engine = build_agent()

    result_state = engine.run(state)
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
