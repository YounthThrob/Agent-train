class FallbackManager:
    def __init__(self, fallback_map):
        self.fallback_map = fallback_map or {}

    def get_fallback_tool(self, tool_name):
        return self.fallback_map.get(tool_name)