from janus.language.block import CodeBlock
from .metric import metric

import multiprocessing
import os
from janus.language.treesitter.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES
from typing import List, Optional, Tuple

from tree_sitter import Node, Parser, Tree


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
        if LANGUAGES[language]["branch_node_types"]:
            self.branch_nodes: List[str] = LANGUAGES[language]["branch_node_types"]
            print(self.branch_nodes)
        else:
            print(f"No branch_node_types defined for language: {language}. \
                Cyclomatic complexity cannot be calculated.")
        print(file)
        # if not os.path.isfile(file):
        #     raise FileNotFoundError
        self.file = file
        self.splitter = TreeSitterSplitter(language=language, protected_node_types=tuple(self.branch_nodes))
        # TODO: Protecting node types will ensure that the splitter doesn't merge node types
        # self.ast = self.splitter.parser.parse(bytes(file, "utf-8"))
        self.ast = self.splitter.split_string(file, name="metrics", prune_unprotected=False)

    def get_complexity(self) -> int:
        return self._traverse_tree(self.ast)

    def _traverse_tree(self, code_block: CodeBlock):
        # TODO: traverse CodeBlock instead of TS Tree
        count = 0
        if code_block.name in self.branch_nodes:
            count += 1
        for item in code_block.children:
            count += self._traverse_tree(item)
        return count

    # def complexity(self):
    #     params = [(file, code) for file, code in self._source_codes()]
    #     with multiprocessing.Pool() as pool:
    #         return pool.map(self._complexity_item, params)


@metric(use_reference=False, help="Cyclomatic complexity score")
def cyclomatic_complexity(
    target: str,
    **kwargs
) -> float:
    """Calculate the cyclomatic complexity score.

    Arguments:
        target: The target text.

    Returns:
        The chrF score.
    """
    language = kwargs["language"]
    score = CyclomaticComplexity(target, language).get_complexity()
    return score 
