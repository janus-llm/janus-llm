import inspect
import json
from typing import Callable

from .cli import evaluate, state


def metric(name: None | str = None, help: None | str = None) -> Callable:
    """Returns a decorator to add a given metric to the cli

    Metrics must follow the format (src_str, cmp_str, **other_params)

    Arguments:
        name: The name of the metric. If None, the function name is used.
        help: The help text for the metric.

    Returns:
        The decorator function.
    """

    def decorator(function):
        def func(*args, **kwargs):
            out = []
            for src, cmp in state["pairs"]:
                out.append(function(src, cmp, *args, **kwargs))
            out_file = state["out_file"]
            with open(out_file, "w") as f:
                json.dump(out, f)

        sig1 = inspect.signature(function)
        sig2 = inspect.signature(func)
        func.__signature__ = sig2.replace(parameters=tuple(sig1.parameters.values())[2:])
        if name is None:
            func.__name__ = function.__name__
        else:
            func.__name__ = name
        if help is None:
            func = evaluate.command()(func)
        else:
            func = evaluate.command(help=help)(func)
        return func

    return decorator
