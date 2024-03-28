from typing import List

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
        self.file = file
        self.splitter = TreeSitterSplitter(
            language=language, protected_node_types=('branch_instruction', 'instruction'))
        # TODO: Protecting node types will ensure that the splitter doesn't merge nodes
        # self.ast = self.splitter.parser.parse(bytes(file, "utf-8"))
        self.ast = self.splitter.split_string(
            file, name="metrics", prune_unprotected=False
        )

    def get_complexity(self) -> int:
        print("Getting complexity...")
        return self._traverse_tree(self.ast)

    def _traverse_tree(self, code_block: CodeBlock):
        count = 0
        print("Traversing tree...")
        print(code_block.name)
        print(code_block.children)
        if code_block.node_type == self.branch_node:
            print(code_block.name)
            count += 1
        for item in code_block.children:
            count += self._traverse_tree(item)
        return count

    # def complexity(self):
    #     params = [(file, code) for file, code in self._source_codes()]
    #     with multiprocessing.Pool() as pool:
    #         return pool.map(self._complexity_item, params)


@metric(use_reference=False, help="Cyclomatic complexity score")
def cyclomatic_complexity(target: str, **kwargs) -> float:
    """Calculate the cyclomatic complexity score.

    Arguments:
        target: The target text.

    Returns:
        The chrF score.
    """
    language = kwargs["language"]
    score = CyclomaticComplexity(target, language).get_complexity()
    return score
