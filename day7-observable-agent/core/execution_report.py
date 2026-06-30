class ExecutionReport:
    @staticmethod
    def build(state):
        return {
            "trace_id": state.trace_id,
            "user_id": state.user_id,
            "user_input": state.user_input,
            "success": len(state.errors) == 0,
            "total_latency": state.total_latency(),
            "total_tokens": state.total_tokens,
            "plan": state.plan,
            "params": state.params,
            "errors": state.errors,
            "warnings": state.warnings,
            "node_metrics": state.node_metrics,
            "tool_metrics": state.tool_metrics,
            "llm_metrics": state.llm_metrics,
            "final_output": state.final_output,
        }

    @staticmethod
    def print_report(state):
        report = ExecutionReport.build(state)

        print("\n========== Execution Report ==========")
        print(f"trace_id: {report['trace_id']}")
        print(f"success: {report['success']}")
        print(f"total_latency: {report['total_latency']}s")
        print(f"total_tokens: {report['total_tokens']}")
        print(f"plan: {report['plan']}")

        print("\n--- Node Metrics ---")
        for item in report["node_metrics"]:
            print(item)

        print("\n--- Tool Metrics ---")
        for item in report["tool_metrics"]:
            print(item)

        print("\n--- Errors ---")
        for err in report["errors"]:
            print("-", err)

        print("\n--- Warnings ---")
        for warning in report["warnings"]:
            print("-", warning)