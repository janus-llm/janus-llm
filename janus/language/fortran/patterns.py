from ...utils.logger import create_logger

log = create_logger(__name__)


NODE_TYPES = [
    "if_statement",
    "do_loop_statement",
    "submodule_statement",
    "function_statement",
    "internal_procedures",
]
