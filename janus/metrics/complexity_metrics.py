import math
from typing import List, Optional

from janus.language.block import CodeBlock
from janus.language.treesitter import TreeSitterSplitter
from janus.metrics.metric import metric
from janus.utils.enums import LANGUAGES


class NodeException(Exception):
    pass


class TreeSitterMetric:
    """A class for calculating node-based complexity metrics of code."""

    def __init__(
        self,
        code: str,
        language: Optional[str],
    ):
        """
        Arguments:
            code: The code to get metrics on
            language: The language the code is written in
        """
        if language is None:
            raise ValueError("Error: must provide language for tree-sitter metrics")
        self.branch_nodes: List[str] = LANGUAGES[language].get("branch_node_types")
        self.operation_nodes: List[str] = LANGUAGES[language].get("operation_node_types")
        self.operand_nodes: List[str] = LANGUAGES[language].get("operand_node_types")
        self.code = code
        self.language = language
        self.splitter = TreeSitterSplitter(
            language=language,
        )
        self.ast = self.splitter._get_ast(code)

    def get_cyclomatic_complexity(self) -> int:
        if not self.branch_nodes:
            raise NodeException(f"No branch nodes are set for {self.language}")
        else:
            return self._count_nodes_of_type(self.ast, self.branch_nodes) + 1

    def get_lines_of_code(self) -> int:
        return self.code.count("\n")

    """
    The following metrics are based on Halstead complexity measures:
    https://en.wikipedia.org/wiki/Halstead_complexity_measures
    """

    def get_program_vocabulary(self) -> int:
        if not self.operation_nodes:
            raise NodeException(f"No operation nodes are set for {self.language}")
        else:
            return self._count_nodes_of_type(
                self.ast, self.operand_nodes, distinct=True
            ) + self._count_nodes_of_type(self.ast, self.operation_nodes, distinct=True)

    def get_program_length(self) -> int:
        if not self.operation_nodes:
            raise NodeException(f"No operation nodes are set for {self.language}")
        else:
            return self._count_nodes_of_type(
                self.ast, self.operation_nodes
            ) + self._count_nodes_of_type(self.ast, self.operand_nodes)

    def get_volume(self) -> float:
        vocabulary = self.get_program_vocabulary()
        if not vocabulary:
            raise ValueError(
                "Volume cannot be calculated because program vocabulary is 0. \
                Confirm that your code is parsing properly."
            )
        return self.get_program_length() * math.log2(vocabulary)

    def get_difficulty(self) -> float:
        return (
            self._count_nodes_of_type(self.ast, self.operation_nodes, distinct=True)
            / 2
            * self._count_nodes_of_type(self.ast, self.operand_nodes, distinct=False)
            / self._count_nodes_of_type(self.ast, self.operand_nodes, distinct=True)
        )

    def get_effort(self) -> float:
        return self.get_volume() * self.get_difficulty()

    def get_time_to_program(self) -> float:
        return self.get_effort() / 18

    def get_num_bugs(self) -> float:
        return self.get_effort() ** (2 / 3) / 3000

    def get_maintainability(self) -> float:
        volume = self.get_volume()
        cyclomatic_complexity = self.get_cyclomatic_complexity()
        lines_of_code = self.get_lines_of_code()
        if not (volume and lines_of_code):
            raise ValueError(
                "Maintainability cannot be calculated because volume or lines of code\
                is 0. Confirm that your code is parsing properly."
            )
        return max(
            0,
            (
                171
                - (5.2 * math.log(volume))
                - (0.23 * cyclomatic_complexity)
                - (16.2 * math.log(lines_of_code))
            )
            * 100
            / 171,
        )

    def _count_nodes_of_type(
        self, code_block: CodeBlock, nodes: List[str], distinct=False
    ) -> int:
        """Recurse through all nodes of a CodeBlock,
        take count of the number of nodes of a specified type"""
        seen_nodes = set()
        count = 0
        nodes_left = [code_block]
        while nodes_left:
            node = nodes_left.pop()
            if str(node.node_type) in nodes:
                if distinct:
                    seen_nodes.add(node.text.strip())
                else:
                    count += 1
            nodes_left.extend(node.children)
        return len(seen_nodes) if distinct else count


@metric(use_reference=False, help="Cyclomatic complexity score")
def cyclomatic_complexity(target: str, **kwargs) -> float:
    """Calculate the cyclomatic complexity score.

    Arguments:
        target: The target text.

    Returns:
        The cyclomatic complexity.
    """
    language = kwargs["language"]
    score = TreeSitterMetric(target, language).get_cyclomatic_complexity()
    return score


@metric(use_reference=False, help="Halstead effort score")
def effort(target: str, **kwargs) -> float:
    """Calculate the Halstead effort.

    Arguments:
        target: The target text.

    Returns:
        The Halstead effort.
    """
    language = kwargs["language"]
    score = TreeSitterMetric(target, language).get_effort()
    return score


@metric(use_reference=False, help="Halstead volume score")
def volume(target: str, **kwargs) -> float:
    """Calculate the Halstead volume.

    Arguments:
        target: The target text.

    Returns:
        The Halstead volume.
    """
    language = kwargs["language"]
    score = TreeSitterMetric(target, language).get_volume()
    return score


@metric(use_reference=False, help="Halstead difficulty score")
def difficulty(target: str, **kwargs) -> float:
    """Calculate the Halstead difficulty.

    Arguments:
        target: The target text.

    Returns:
        The Halstead difficulty.
    """
    language = kwargs["language"]
    score = TreeSitterMetric(target, language).get_difficulty()
    return score


@metric(use_reference=False, help="Maintainability score")
def maintainability(target: str, **kwargs) -> float:
    """Calculate the maintainability score.

    Arguments:
        target: The target text.

    Returns:
        The maintainability score.
    """
    language = kwargs["language"]
    score = TreeSitterMetric(target, language).get_maintainability()
    return score
