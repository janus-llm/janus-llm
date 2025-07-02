import json

from janus.language.block import CodeBlock
from janus.retrievers.retriever import JanusRetriever
from janus.utils.logger import create_logger

log = create_logger(__name__)


class OpCodeRetriever(JanusRetriever):
    def __init__(self, opcode_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(opcode_filename, "r") as f:
            self._op_code_dict = json.load(f)

    def get_context(self, code_block: CodeBlock) -> str:
        context = ""
        for line in code_block.text.split("\n"):
            stripped_line = line.strip()
            if stripped_line == "":
                continue
            if stripped_line[0] == "*":
                continue
            if line[0] == " ":
                op_code = stripped_line.split()[0]
            else:
                if len(stripped_line.split()) == 1:
                    continue
                op_code = stripped_line.split()[1]
            if op_code not in self._op_code_dict:
                log.debug(f"Error: op code {op_code} not found")
                continue
            context += f"{op_code}: {self._op_code_dict[op_code]}\n"
        return context
