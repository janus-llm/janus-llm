from typing import List

from janus.converter.converter import Converter


class Aggregator(Converter):
    def __init__(
        self,
        aggregator_prompt: str,
        intermediate_converters: List[Converter],
        separator: str = "\n==============\n",
        **kwargs,
    ):
        self._aggregator_prompt_name = aggregator_prompt
        self._intermediate_converters = intermediate_converters
        self._separator = separator
        super().__init__(**kwargs)
        self._load_parameters()

    def _load_agregator_prompt(self):
        pass

    def _load_parameters(self) -> None:
        super()._load_parameters()
        self._load_agregator_prompt()
