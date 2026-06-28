class DAGEngine:
    def __init__(self,nodes):
        self.nodes = nodes

    def run(self, state):
        for node in self.nodes:
            print(f"\n========== 执行节点: {node.name} ==========")

            try:
                state = node.run(state)
            except Exception as e:
                state.add_error(f"Error in node '{node.name}': {str(e)}")
                print(f"Error in node '{node.name}': {str(e)}")
                break  # Stop execution on error

            if state.errors:
                print("检测到错误，停止执行。")
                break  # Stop execution if there are errors
        return state