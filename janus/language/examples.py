import os

import janus

CODE_EXAMPLE_FILES = {
    "python": os.path.join(
        os.path.dirname(janus.__file__), "language/example_source_codes/example.py"
    ),
    "fortran": os.path.join(
        os.path.dirname(janus.__file__), "language/example_source_codes/example.f90"
    ),
    "mumps": os.path.join(
        os.path.dirname(janus.__file__), "language/example_source_codes/example.m"
    ),
}
