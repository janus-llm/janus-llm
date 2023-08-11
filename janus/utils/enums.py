from typing import Dict, Tuple

VALID_SOURCE_LANGUAGES: Tuple[str, ...] = (
    "fortran",
    "mumps",
)
VALID_TARGET_LANGUAGES: Tuple[str, ...] = ("python", "mumps", "text")
LANGUAGE_COMMENTS: Dict[str, str] = {
    "fortran": "!",
    "python": "#",
    "mumps": ";",
    "text": "|",
}
LANGUAGE_SUFFIXES: Dict[str, str] = {
    "fortran": "f90",
    "python": "py",
    "mumps": "m",
    "text": "txt",
}
