from typing import Any, Callable


def _passthrough_decorator(_str: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return func

    return decorator


def step(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return _passthrough_decorator(name)


def title(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return _passthrough_decorator(name)