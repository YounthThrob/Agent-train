import json
import re
from llm import LLM
from core.tool_router import ToolRouter
# from prompt import SYSTEM_PROMPT
from prompt_ReAct import SYSTEM_PROMPT

tool_router = ToolRouter()
llm = LLM()

# LLM输出解析器
def parse_react(text: str):
    thought = re.findall(r"Thought:(.*)", text)
    action = re.findall(r"Action:(.*)", text)
    action_input = re.findall(r"Action Input:(.*)", text)
    final = re.findall(r"Final Answer:(.*)", text)

    return {
        "thought": thought[-1].strip() if thought else None,
        "action": action[-1].strip() if action else None,
        "input": action_input[-1].strip() if action_input else None,
        "final": final[-1].strip() if final else None
    }


def parse_tool(response: str):

    print("\n[DEBUG LLM RAW]:", response)

    try:
        data = json.loads(response)
    except Exception:
        print("❌ JSON解析失败")
        return None, None

    if not isinstance(data, dict):
        print("❌ 非dict结构")
        return None, None

    tool_name = data.get("tool")
    tool_input = data.get("input")

    if tool_name is None:
        print("❌ 没有tool字段")
        return None, None

    if tool_name == "none":
        return None, None

    return tool_name, tool_input

# run ReAct Agent
def run_react_agent(user_input):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    for step in range(5):  # 防死循环

        response = llm.chat(messages)
        content = response["content"]

        print(f"\n[Step {step} LLM]:\n", content)

        parsed = parse_react(content)

        # 🟢 终止条件
        if parsed["final"]:
            print("\n✅ Final Answer:", parsed["final"])
            return parsed["final"]

        # 🟡 执行工具
        if parsed["action"] and parsed["action"] != "none":

            tool_result = tool_router.router(
                parsed["action"],
                parsed["input"]
            )

            print("\n🔧 Tool Result:", tool_result)

            # Observation回填
            messages.append({
                "role": "assistant",
                "content": content
            })

            messages.append({
                "role": "user",
                "content": f"Observation: {tool_result}"
            })

        else:
            print("\n⚠️ 无Action，退出")
            return content

    return "❌ 达到最大步数"

# run Agent(based on tool selection)
def run_agent(user_input: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    response = llm.chat(messages)

    content = response["content"]   # ✔ 必须取string

    tool_name, tool_input = parse_tool(content)

    if tool_name:

        tool_result = tool_router.router(tool_name, tool_input)

        print("\n工具结果:", tool_result)

        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "user",
            "content": f"工具结果: {tool_result['result']}"
        })
        print("\n[DEBUG MESSAGES]:", messages)

        final = llm.chat(messages)

        print("\n最终输出:", final["content"])

    else:

        print("\n直接回答:", content)

if __name__ == "__main__":

    while True:
        user_input = input("\n请输入问题（exit退出）: ")

        if user_input == "exit":
            break

        # run_agent(user_input)
        run_react_agent(user_input)