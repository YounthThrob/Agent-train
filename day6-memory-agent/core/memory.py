from datetime import datetime
from typing import Any, Dict, List, Optional

class MemoryManager:
    def __init__(self, store):
        self.store = store

    def load(self,state):
        """ 执行前加载用户记忆"""
        memory = self.store.load_user_memory(state.user_id)
        state.memory = memory

        state.add_trace("MemoryManager.load", {
            "user_id": state.user_id,
            "memory": memory
        })

        return state
    
    def save(self,state):
        """ 执行后保存用户记忆"""
        memory = state.memory or {
            "profile": {},
            "preferences": {},
            "history": []
        }

        # 1. 更新用户偏好/常用信息
        self._update_preferences(memory, state)

        # 2. 保存用户本次执行历史
        self._update_history(memory, state)

        # 3. 持久化
        self.store.save_user_memory(state.user_id, memory)

        state.add_trace("memory_save", {
            "user_id": state.user_id,
            "memory": state.memory
        })

        return state
    
    def _update_preferences(self, memory: Dict[str, Any], state):
        """ 更新用户偏好/常用信息 """
        preferences = memory.setdefault("preferences", {})
        # 这里可以根据state中的信息更新用户偏好
        # 例如：
        city = state.params.get("city")
        expense_type = state.params.get("expense_type")
        if city:
            preferences["common_city"] = city
        if expense_type:
            preferences["common_expense_type"] = expense_type

    def _update_history(self, memory: Dict[str, Any], state):
        """ 更新用户执行历史 """
        history = memory.setdefault("history", [])
        # 这里可以根据state中的信息更新用户执行历史
        history_entry = {
            "time": datetime.now().isoformat(timespec='seconds'),
            "user_input": state.user_input,
            "params": state.params,
            "plan": state.plan,
            "final_output": state.final_output,
            "errors": state.errors,
            "warnings": state.warnings
        }

        # 只保留最近20条历史
        memory["history"] = history[-20:]