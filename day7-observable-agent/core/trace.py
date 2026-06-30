import time
from contextlib import contextmanager

@contextmanager
def trace_span(state,span_type: str, span_name: str):
    """
    记录某一段执行耗时
    span_type 示例：
    - "node"
    - "tool"
    - "llm"
    - "memory"
    - "validation"
    """
    start_time = time.time()
    try:
        yield
        success = True
        error = None
    except Exception as e:
        success = False
        error = str(e)
        raise
    finally:
        end_time = time.time()
        lantency = round(end_time - start_time, 4)
        record = {
            "trace_id": state.trace_id,
            "type": span_type,
            "name": span_name,
            "sucess": success,
            "latency": lantency,
            "error": error,
            "start_time": start_time,
            "end_time": end_time
        }

        if span_type == "node":
            state.node_metrics.append(record)
        elif span_type == "tool":
            state.tool_metrics.append(record)
        elif span_type == "llm":
            state.llm_metrics.append(record)
        
        state.add_trace(f"{span_type}:{span_name}", record)