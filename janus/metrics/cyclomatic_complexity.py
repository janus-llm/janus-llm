import typer
from sacrebleu import sentence_chrf

from .metric import metric

import multiprocessing
import os
from typing import List, Optional, Tuple

from tree_sitter import Node, Parser, Tree


# This code is adapted from on: https://github.com/frite/mccabe
class Mccabe:
    suffixes: Tuple[str, ...]
    language: Lang
    judge_nodes: List[str]

    def __init__(
        self,
        directory: Optional[str] = None,
        file: Optional[str] = None,
    ):
        """
        The order of param is source > file > directory
        :param directory: The source language
        :param file: The source code file
        """
        if not any([directory, file]):
            pass
            # TODO: error handling
        self.directory = directory
        self.file = file

    def _source_codes(self):
        if self.file:
            with open(self.file) as f:
                yield self.file, f.read()
        elif self.directory:
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    if not file.endswith(self.suffixes):
                        continue
                    path = os.path.join(root, file)
                    with open(path) as f:
                        yield path, f.read()

    def _visit_node(self, node: Node):
        count = 0
        if node.type in self.judge_nodes:
            count += 1
        for item in node.children:
            count += self._visit_node(item)
        return count

    def _complexity_item(self, args: Tuple[str, str]):
        file, code = args
        parser = Parser()
        parser.set_language(self.language.get_lib())
        tree = parser.parse(code.encode())  # type:Tree
        return file, self._visit_node(tree.root_node)

    def complexity(self):
        params = [(file, code) for file, code in self._source_codes()]
        with multiprocessing.Pool() as pool:
            return pool.map(self._complexity_item, params)

    def run(self):
        ret = {}
        for file, count in self.complexity():
            ret[file] = count
        return ret


@metric(help="chrF score using Torchmetrics")
def chrf(
    target: str,
    reference: str,
    n_char_order: int = typer.Option(
        default=6,
        help=(
            "A character n-gram order. If n_char_order=6, the metrics refers to the "
            "official chrF/chrF++."
        ),
    ),
    n_word_order: int = typer.Option(
        default=2,
        help=(
            "A word n-gram order. If n_word_order=2, the metric refers to the official "
            "chrF++. If n_word_order=0, the metric is equivalent to the original ChrF."
        ),
    ),
    beta: float = typer.Option(
        default=2.0,
        help=(
            "Determines importance of recall w.r.t. precision. If beta=1, their "
            "importance is equal."
        ),
    ),
) -> float:
    """Calculate the chrF Score using Torchmetrics.

    Arguments:
        target: The target text.
        reference: The reference text.
        n_char_order: The character order.
        n_word_order: The word order.
        beta: The beta value.

    Returns:
        The chrF score.
    """
    score = sentence_chrf(
        target,
        [reference],
        char_order=n_char_order,
        word_order=n_word_order,
        beta=beta,
    )
    return float(score.score)
