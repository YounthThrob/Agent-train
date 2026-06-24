import json
from llm import LLM
from core.tool_router import ToolRouter
from prompt import SYSTEM_PROMPT

tool_router = ToolRouter()
llm = LLM()


def parse_tool(response: str):

    import json

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

        final = llm.chat(messages)

        print("\n最终输出:", final["content"])

    else:

        print("\n直接回答:", content)

if __name__ == "__main__":

    while True:
        user_input = input("\n请输入问题（exit退出）: ")

        if user_input == "exit":
            break

        run_agent(user_input)