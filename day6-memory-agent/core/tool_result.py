from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class ToolResult:
    success: bool
    result: Any = None
    error: Optional[str] = None

    tool_name: Optional[str] = None
    used_fallback: bool = False
    retry_count: int = 0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "tool_name": self.tool_name,
            "used_fallback": self.used_fallback,
            "retry_count": self.retry_count,
            "metadata": self.metadata,
        }