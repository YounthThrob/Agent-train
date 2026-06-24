from llm import SimpleLLM

def run_agent():
    llm = SimpleLLM()
    print("智能体助手已启动。输入 'exit' 退出。")
    
    while True:
        user_input = input("用户: ")
        if user_input.lower() == 'exit':
            print("智能体助手已退出。")
            break
        
        response = llm.chat(user_input)
        print(f"助手: {response['content']}")
        print(f"Token数量: {response['token']}")

if __name__ == "__main__":
    run_agent()