from core.trace import trace_span
from core.logger import get_logger

logger = get_logger(__name__)

class DynamicDAGEngine:
    def __init__(self, node_registry, validator,repair_manager):
        """
        node_registry 示例：
        {
            "param_node": ParamNode(...),
            "policy_node": PolicyNode(...),
            "amount_check_node": AmountCheckNode(...),
            "risk_node": RiskNode(...),
            "final_node": FinalNode(...)
        }
        """
        self.node_registry = node_registry
        self.validator = validator
        self.repair_manager = repair_manager

    def run(self, state):
        if not state.plan:
            state.add_error("执行计划为空")
            return state

        if self.validator:
            ok, err = self.validator.validate_plan(state.plan)
            if not ok:
                state.add_error(f"Plan 校验失败: {err}")
                return state

        for node_name in state.plan:
            print(f"\n========== 动态执行节点: {node_name} ==========")
            logger.info(f"[{state.trace_id}] start node: {node_name}")

            node = self.node_registry.get(node_name)

            if node is None:
                state.add_error(f"节点未注册: {node_name}")
                logger.error(f"[{state.trace_id}] node not registered: {node_name}")
                break

            # 节点输入校验
            if self.validator:
                with trace_span(state, "validation", f"{node_name}:input"):
                    ok, err = self.validator.validate_node_input(node_name, state)

                if not ok:
                    logger.warning(
                        f"[{state.trace_id}] node input validation failed: {err}"
                    )

                    repaired = False

                    if self.repair_manager and state.repair_count < state.max_repair_count:
                        state.repair_count += 1

                        with trace_span(state, "repair", f"{node_name}:repair_params"):
                            repaired = self.repair_manager.repair_params(state)

                    if repaired:
                        logger.info(
                            f"[{state.trace_id}] repair success, revalidate node: {node_name}"
                        )

                        with trace_span(state, "validation", f"{node_name}:input_recheck"):
                            ok, err = self.validator.validate_node_input(node_name, state)

                    if not ok:
                        state.add_error(f"节点输入校验失败且无法修复: {err}")
                        break

            # 节点执行
            try:
                with trace_span(state, "node", node_name):
                    before_errors = len(state.errors)
                    state = node.run(state)

                    if len(state.errors) > before_errors:
                        logger.error(
                            f"[{state.trace_id}] node error: {node_name}, errors={state.errors}"
                        )
                        break

            except Exception as e:
                state.add_error(f"{node_name} 执行异常: {str(e)}")
                logger.exception(f"[{state.trace_id}] node exception: {node_name}")
                break

            # 节点输出校验
            if self.validator:
                output = self._get_node_output(node_name, state)

                with trace_span(state, "validation", f"{node_name}:output"):
                    ok, err = self.validator.validate_node_output(node_name, output)

                if not ok:
                    state.add_error(f"节点输出校验失败: {err}")
                    logger.error(
                        f"[{state.trace_id}] node output validation failed: {err}"
                    )
                    break

            logger.info(f"[{state.trace_id}] finish node: {node_name}")

        return state

    def _get_node_output(self, node_name, state):
        if node_name == "policy_node":
            return state.policy_result

        if node_name == "amount_check_node":
            return state.amount_check_result

        if node_name == "risk_node":
            return state.risk_result

        return {}
    