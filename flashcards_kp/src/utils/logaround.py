import inspect
import logging
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def log_around[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    """Log function input parameters and return value."""
    signature = inspect.signature(fn)
    callable_name = fn.__qualname__  # ty: ignore[unresolved-attribute]
    func_logger = logging.getLogger(fn.__module__)

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        params = {name: repr(value) for name, value in bound.arguments.items()}
        func_logger.debug("Calling %s", callable_name, extra={"params": params}) 

        result = fn(*args, **kwargs)
        func_logger.debug("Returned %s", callable_name, extra={"output": repr(result)})  
        return result

    return wrapper

