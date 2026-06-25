from core.node import BaseNode

class IntentNode(BaseNode):
    name = "IntentNode"

    def run(self, state):
        # 使用 LLM 进行意图识别
        # Day3先写死，重点学习DAG的执行流程，后续再完善
        if "报销"  in state.user_input:
            state.intent = "expense_check"
        else:
            state.intent = "unknown"

        state.add_trace(self.name, {"intent": state.intent})
        if state.intent == "unknown":
            state.add_error("无法识别用户意图。")
        
        return state