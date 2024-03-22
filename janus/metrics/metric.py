import inspect
import json
from typing import Optional

from .cli import evaluate, state


def metric(name: Optional[str] = None, help: Optional[str] = None):
    """
    Returns a decorator to add a given metric to the cli
    metrics must follow the format (src_str, cmp_str, **other_params)
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
