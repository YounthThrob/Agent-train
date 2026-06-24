import json
from llm import LLM
from core.tool_router import ToolRouter
from prompt import SYSTEM_PROMPT

tool_router = ToolRouter()
llm = LLM()


def parse_tool(response: str):

    try:
        data = json.loads(response)

        tool_name = data.get("tool")
        tool_input = data.get("input")

        print(f"解析工具: {tool_name}, input: {tool_input}")

        return tool_name, tool_input

    except json.JSONDecodeError:
        return None, None


def run_agent(user_input: str):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    # 1️⃣ LLM调用
    response = llm.chat(messages)

    content = response["content"]   # ✔ 关键修复

    print("\nLLM响应:", content)

    # 2️⃣ 解析工具
    tool_name, tool_input = parse_tool(content)

    # 3️⃣ 如果需要工具
    if tool_name:

        tool_result = tool_router.router(tool_name, tool_input)

        print("\n工具调用结果:", tool_result)

        # 4️⃣ 回填LLM（必须string）
        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "user",
            "content": f"工具结果: {tool_result}"
        })

        final_response = llm.chat(messages)

        print("\n最终LLM响应:", final_response["content"])

    else:

        print("\n无需调用工具，直接输出:", content)


if __name__ == "__main__":

    while True:
        user_input = input("\n请输入问题（exit退出）: ")

        if user_input == "exit":
            break

        run_agent(user_input)