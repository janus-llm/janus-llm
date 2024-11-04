from janus.llm.models_info import JanusModel
from janus.parsers.parser import JanusParser
from janus.refiners.refiner import ReflectionRefiner


class ALCFixUMLVariablesRefiner(ReflectionRefiner):
    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
    ):
        super().__init__(
            llm=llm,
            parser=parser,
            max_retries=max_retries,
            prompt_template_name="refinement/uml/alc_fix_variables",
        )


class FixUMLConnectionsRefiner(ReflectionRefiner):
    def __init__(
        self,
        llm: JanusModel,
        parser: JanusParser,
        max_retries: int,
    ):
        super().__init__(
            llm=llm,
            parser=parser,
            max_retries=max_retries,
            prompt_template_name="refinement/uml/fix_connections",
        )
