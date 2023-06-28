from ...utils.logger import create_logger
from ..node import NodeTypes

log = create_logger(__name__)


NODE_TYPES: NodeTypes = (
    "if_statement",
    "do_loop_statement",
    "submodule_statement",
    "function_statement",
    "internal_procedures",
)
