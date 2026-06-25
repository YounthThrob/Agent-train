# Base class for all nodes in the DAG
class BaseNode:
    def __init__(self,llm=None,tool_router=None):
        self.llm = llm
        self.tool_router = tool_router
    
    def run(self, state):
        raise NotImplementedError("Subclasses must implement the run method.")