from janus.language.block import CodeBlock
from janus.language.treesitter.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES

from .metric import metric


class BranchNodeException(Exception):
    pass


class CyclomaticComplexity:
    """A class for calculating cyclomatic complexity of code."""

    def __init__(
        self,
        code: str,
        language: str,
    ):
        """
        Arguments:
            code: The code to get metrics on
            language: The language the code is written in
        """
        if LANGUAGES[language]["branch_node_type"]:
            self.branch_node = LANGUAGES[language]["branch_node_type"]
            print(self.branch_node)
        else:
            raise BranchNodeException(
                f"No branch nodes defined in utils/enums.py for {language}."
            )
        self.code = code
        self.splitter = TreeSitterSplitter(
            language=language, protected_node_types=("branch_instruction", "instruction")
        )
        self.ast = self.splitter.split_string(
            code, name="metrics", prune_unprotected=False
        )

    def get_complexity(self) -> int:
        return self._traverse_tree(self.ast) + 1

    def _traverse_tree(self, code_block: CodeBlock) -> int:
        """Recurse through all nodes of a CodeBlock, take count of the number of branch
        nodes"""
        count = 0
        if code_block.node_type == self.branch_node:
            count += 1
        for item in code_block.children:
            count += self._traverse_tree(item)
        return count


@metric(use_reference=False, help="Cyclomatic complexity score")
def cyclomatic_complexity(target: str, **kwargs) -> float:
    """Calculate the cyclomatic complexity score.

    Arguments:
        target: The target text.

    Returns:
        The cyclomatic complexity.
    """
    language = kwargs["language"]
    score = CyclomaticComplexity(target, language).get_complexity()
    return score
