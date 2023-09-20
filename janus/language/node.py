import dataclasses
from typing import NewType, Tuple, List, ForwardRef, Optional
import tree_sitter

from ..utils.logger import create_logger

log = create_logger(__name__)


NodeType = NewType("NodeType", str)
NodeTypes = NewType("NodeTypes", Tuple[NodeType, ...])


@dataclasses.dataclass
class ASTNode(object):
    text: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    start_byte: int
    end_byte: int
    prefix: str
    suffix: str
    type: NodeType
    children: List[ForwardRef("ASTNode")]
    name: Optional[str] = None

    @classmethod
    def from_tree_sitter_node(cls, node: tree_sitter.Node, original: bytes) -> ForwardRef("ASTNode"):
        prefix_start = 0
        if node.prev_sibling is not None:
            prefix_start = node.prev_sibling.end_byte
        elif node.parent is not None:
            prefix_start = node.parent.start_byte

        suffix_end = len(original)
        if node.next_sibling is not None:
            suffix_end = node.next_sibling.start_byte
        elif node.parent is not None:
            suffix_end = node.parent.end_byte

        children = [cls.from_tree_sitter_node(child, original) for child in node.children]

        return cls(
            text=node.text.decode(),
            name=node.id,
            start_point=node.start_point,
            end_point=node.end_point,
            start_byte=node.start_byte,
            end_byte=node.end_byte,
            prefix=str(original[prefix_start:node.start_byte]),
            suffix=str(original[node.end_byte:suffix_end]),
            type=node.type,
            children=children
        )

    @classmethod
    def merge_nodes(cls, nodes: List[ForwardRef("ASTNode")]) -> ForwardRef("ASTNode"):
        if len(nodes) == 1:
            return nodes[0]

        interleaved = [s for node in nodes for s in [node.text, node.suffix]]
        text = ''.join(interleaved[:-1])
        return cls(
            text=text,
            name=f"{nodes[0].name}:{nodes[-1].name}",
            start_point=nodes[0].start_point,
            end_point=nodes[-1].end_point,
            start_byte=nodes[0].start_byte,
            end_byte=nodes[-1].end_byte,
            prefix=nodes[0].prefix,
            suffix=nodes[-1].suffix,
            type=NodeType("merge"),
            children=sum([node.children for node in nodes], [])
        )