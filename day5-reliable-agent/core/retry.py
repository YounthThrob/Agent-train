import time
from typing import Callable, Tuple, Any

class RetryManager:
    def __init__(
            self,
            max_retries: int = 3,
            base_delay: float = 0.5,
            max_delay: float = 5.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def run(self,func: Callable,*args, **kwargs) -> Tuple[bool, Any, int, str | None]:
        """
        Executes a function with retry logic.

        :param func: The function to execute.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        :return: A tuple containing a boolean indicating success and the result or error message.
        """
        last_error = None

        for attempt in range(self.max_retries +1 ):
            try:
                result = func(*args, **kwargs)
                return True, result, attempt, None
            except Exception as e:
                last_error = str(e)
                if attempt > self.max_retries:
                    break
                # 指数级退避重试
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                time.sleep(delay)
        return False, last_error, self.max_retries, last_error