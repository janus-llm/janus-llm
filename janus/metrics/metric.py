import inspect
import json

from .cli import evaluate, state


def metric():
    def decorator(function):
        def func(*args, **kwargs):
            src_file = state["src_file"]
            cmp_file = state["cmp_file"]
            with open(src_file, "r") as f:
                src = f.read()
            with open(cmp_file, "r") as f:
                cmp = f.read()
            out = function(src, cmp, *args, **kwargs)
            res = {f"{src_file}_{cmp_file}_{function.__name__}": float(out)}
            out_file = state["out_file"]
            with open(out_file, "w") as f:
                json.dump(res, f)

        sig1 = inspect.signature(function)
        sig2 = inspect.signature(func)
        func.__signature__ = sig2.replace(parameters=tuple(sig1.parameters.values())[2:])
        func.__name__ = function.__name__
        func = evaluate.command()(func)
        return func

    return decorator
