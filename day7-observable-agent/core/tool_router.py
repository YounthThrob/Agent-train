from tools.amount_tool import check_amount_limit
from tools.policy_tool import query_policy
from tools.risk_tool import check_risk
from tools.backup_policy_tool import query_policy_backup
from core.retry import RetryManager
from core.fallback import FallbackManager
from core.tool_result import ToolResult

class ToolRouter:
    def __init__(self):
        self.tools = {
            "check_amount_limit": check_amount_limit,
            "query_policy": query_policy,
            "check_risk": check_risk,
            "query_policy_backup": query_policy_backup
        }
        self.retry_manager = RetryManager(
            max_retries=3,
            base_delay=0.5,
            max_delay=3.0
        )

        self.fallback_manager = FallbackManager(
            fallback_map={
                "query_policy": "query_policy_backup"
            }
        )

    def route(self, tool_name, tool_input):
        """
        可靠工具调用入口：
        1. 检查工具是否存在
        2. 主工具重试
        3. 主工具失败后尝试备用工具
        4. 返回统一结构ToolResult
        """
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                result=None,
                error=f"Tool '{tool_name}' not found",
                tool_name=tool_name
            ).to_dict()
        
        # 1. 主工具调用,带重试
        success, result, error, retry_count = self.retry_manager.run(
            self.tools[tool_name], tool_input
        )
        if success:
            return ToolResult(
                success=True,
                result=result,
                error=None,
                tool_name=tool_name,
                used_fallback=False,
                retry_count=retry_count
            ).to_dict()
        # 2. 主工具失败后尝试备用工具
        fallback_tool_name = self.fallback_manager.get_fallback_tool(tool_name)
        if fallback_tool_name and fallback_tool_name in self.tools:
            print(f"主工具 '{tool_name}' 调用失败，尝试备用工具 '{fallback_tool_name}'")
            fallback_success, fallback_result, fallback_retry_count, fallback_error = self.retry_manager.run(
                self.tools[fallback_tool_name], tool_input
            )
            if fallback_success:
                return ToolResult(
                    success=True,
                    result=fallback_result,
                    error=None,
                    tool_name=fallback_tool_name,
                    used_fallback=True,
                    retry_count=fallback_retry_count,
                    metadata={
                        "original_tool": tool_name,
                        "original_error": error}
                ).to_dict()
            return ToolResult(
                success=False,
                result=None,
                error=f"主工具调用失败 '{tool_name}'Fallback error: {fallback_error}",
                tool_name=tool_name,
                used_fallback=True,
                retry_count=retry_count + fallback_retry_count,
            ).to_dict()
        # 3. 没有fallback
        return ToolResult(
            success=False,
            result=None,
            error=error,
            tool_name=tool_name,
            used_fallback=False,
            retry_count=retry_count
        ).to_dict()