import inspect

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
            return function(src, cmp, *args, **kwargs)

        sig1 = inspect.signature(function)
        sig2 = inspect.signature(func)
        func.__signature__ = sig2.replace(parameters=tuple(sig1.parameters.values())[2:])
        func.__name__ = function.__name__
        func = evaluate.command()(func)
        return func

    return decorator
