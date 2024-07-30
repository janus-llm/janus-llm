from janus.converter.converter import Converter
from janus.language.combine import JsonCombiner
from janus.parsers.eval_parser import EvaluationParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Evaluator(Converter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_prompt("evaluate")
        self._combiner = JsonCombiner()
        self._parser = EvaluationParser()
        self._load_parameters()
