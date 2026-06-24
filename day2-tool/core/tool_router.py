from tools.calculator import calculator
from tools.search import search

class ToolRouter:

    def __init__(self):
        self.tools = {
            "calculator": calculator,
            "search": search
        }

    def router(self, tool_name: str, tool_input: str):

        if tool_name not in self.tools:

            return {
                "success": False,
                "result": None,
                "error": f"Tool {tool_name} not found"
            }

        try:
            result = self.tools[tool_name](tool_input)

            return {
                "success": True,
                "result": result,
                "error": None
            }

        except Exception as e:

            return {
                "success": False,
                "result": None,
                "error": str(e)
            }