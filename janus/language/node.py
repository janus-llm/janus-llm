from typing import NewType, Tuple

from janus.utils.logger import create_logger

log = create_logger(__name__)


NodeType = NewType("NodeType", str)
NodeTypes = NewType("NodeTypes", Tuple[NodeType, ...])
