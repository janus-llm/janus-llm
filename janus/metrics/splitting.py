from typing import Callable

SPLITTING_METHODS: dict[str, Callable[[str, str], list[str]]] = {}


def register_splitting_method(name: None | str = None) -> Callable[[Callable], Callable]:
    """Registers a pairing method for splitting strings in files

    Arguments:
        name: The name of the splitting method. If None, the function name is used.
        help: The help text for the pairing method.

    Returns:
        The decorator function.
    """

    def decorator(f: Callable[[str, str], list[tuple[str, str]]]):
        if name is None:
            splitting_name = f.__name__
        else:
            splitting_name = name
        SPLITTING_METHODS[splitting_name] = f
        return f

    return decorator


@register_splitting_method(name="file")
def split_by_file(src: str, **kwargs) -> list[str]:
    """Split the source text by file

    Arguments:
        src: The source text.

    Returns:
        A list of strings.
    """
    return [src]
