from langchain.schema.language_model import BaseLanguageModel

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.node import NodeType
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.logger import create_logger

log = create_logger(__name__)


class AlcCombiner(Combiner):
    """A class that combines code blocks into ALC files."""

    def __init__(self) -> None:
        """Initialize a AlcCombiner instance."""
        super().__init__("ibmhlasm")


class AlcSplitter(TreeSitterSplitter):
    """A class for splitting ALC code into functional blocks to prompt
    with for transcoding.
    """

    def __init__(
        self,
        model: None | BaseLanguageModel = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        prune_unprotected: bool = False,
    ):
        """Initialize a AlcSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language="ibmhlasm",
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
        )

    def _get_ast(self, code: str) -> CodeBlock:
        root = super()._get_ast(code)

        # Current treesitter implementation does not nest csects and dsects
        # The loop below nests nodes following csect/dsect instructions into
        #  the children of that instruction
        sect_types = {"csect_instruction", "dsect_instruction"}
        queue: list[CodeBlock] = [root]
        while queue:
            block = queue.pop(0)

            # Search this children for csects and dsects. Create a list of groups
            #  where each group is a csect or dsect, starting with the csect/dsect
            #  instruction and containing all the subsequent nodes up until the
            #  next csect or dsect instruction
            sects: list[list[CodeBlock]] = [[]]
            for c in block.children:
                if c.node_type in sect_types:
                    sects.append([c])
                else:
                    sects[-1].append(c)

            sects = [s for s in sects if s]

            # Restructure the tree, making the head of each group the parent
            #  of all the remaining nodes in that group
            if len(sects) > 1:
                block.children = []
                for sect in sects:
                    if sect[0].node_type in sect_types:
                        sect_node = self.merge_nodes(sect)
                        sect_node.children = sect
                        sect_node.node_type = NodeType(str(sect[0].node_type)[:5])
                        block.children.append(sect_node)
                    else:
                        block.children.extend(sect)

            # Push the children onto the queue
            queue.extend(block.children)

        return root
