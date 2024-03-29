from janus.language.block import CodeBlock
from janus.language.treesitter.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES

from .metric import metric


class CyclomaticComplexity:
    def __init__(
        self,
        file: str,
        language: str,
    ):
        """
        The order of param is source > file > directory
        :param directory: The source language
        :param file: The source code file
        """
        if LANGUAGES[language]["branch_node_type"]:
            self.branch_node = LANGUAGES[language]["branch_node_type"]
            print(self.branch_node)
        else:
            print(
                f"No branch_node_types defined for language: {language}. \
                Cyclomatic complexity cannot be calculated."
            )
            exit(1)
        self.file = file
        self.splitter = TreeSitterSplitter(
            language=language, protected_node_types=("branch_instruction", "instruction")
        )
        self.ast = self.splitter.split_string(
            file, name="metrics", prune_unprotected=False
        )

    def get_complexity(self) -> int:
        print("Getting complexity...")
        return self._traverse_tree(self.ast)

    def _traverse_tree(self, code_block: CodeBlock) -> int:
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
