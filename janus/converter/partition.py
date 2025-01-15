from janus.converter.converter import Converter
from janus.parsers.partition_parser import PartitionParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Partitioner(Converter):
    def __init__(self, partition_token_limit: int, **kwargs):
        super().__init__(**kwargs)
        self.set_prompts("partition")
        self._load_model()
        self._parser = PartitionParser(
            token_limit=partition_token_limit,
            model=self._llm,
        )
        self._target_language = self._source_language
        self._target_suffix = self._source_suffix
        self._load_parameters()
