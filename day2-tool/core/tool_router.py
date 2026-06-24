from tools.calculator import calculator
from tools.search import search

class ToolRouter:

    def __init__(self):

        self.tools = {
            "calculator": self._wrap(calculator),
            "search": self._wrap(search)
        }

    def _wrap(self, func):

        def wrapper(tool_input):

            try:
                result = func(tool_input)

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

        return wrapper

    def router(self, tool_name: str, tool_input: str):

        if tool_name not in self.tools:

            return {
                "success": False,
                "result": None,
                "error": f"Tool '{tool_name}' not found"
            }

        return self.tools[tool_name](tool_input)