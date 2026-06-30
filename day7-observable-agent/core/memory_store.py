import json
import os
from typing import Dict, Any

class JSONMemoryStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            self._write({})
        
    def _read(self) -> Dict[str, Any]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def _write(self, data: Dict[str, Any]):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_user_memory(self, user_id: str) -> Dict[str, Any]:
        data = self._read()
        return data.get(user_id, {
            "profile": {},
            "preferences": {},
            "history": []
        })
    
    def save_user_memory(self, user_id: str, memory: Dict[str, Any]):
        data = self._read()
        data[user_id] = memory
        self._write(data)