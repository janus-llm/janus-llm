import inspect
import json

from .cli import evaluate, state


def metric():
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
        func.__name__ = function.__name__
        func = evaluate.command()(func)
        return func

    return decorator
