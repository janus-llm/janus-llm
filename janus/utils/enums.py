from typing import Dict, Tuple

VALID_SOURCE_LANGUAGES: Tuple[str, ...] = ("fortran",)
VALID_TARGET_LANGUAGES: Tuple[str, ...] = ("python",)
LANGUAGE_SUFFIXES: Dict[str, str] = {"fortran": "f90", "python": "py"}
