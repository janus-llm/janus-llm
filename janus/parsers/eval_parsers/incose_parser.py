import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal, List
from janus.language.block import CodeBlock
from ...utils.logger import create_logger
from janus.parsers.parser import JanusParser
from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage

log = create_logger(__name__)

class Criteria(BaseModel):
    reasoning: str
    score: Literal["pass", "fail"]

class Requirement(BaseModel):
    requirement: str
    C1: Criteria
    C2: Criteria
    C3: Criteria
    C4: Criteria
    C5: Criteria
    C6: Criteria
    C7: Criteria
    C8: Criteria
    C9: Criteria

class RequirementList(BaseModel):
    requirements: List[Requirement]

class IncoseParser(PydanticOutputParser, JanusParser):
    block_name: str = ""
    input_length: int = 0  # Define input_length as a Pydantic field with a default value

    def __init__(self):
        super().__init__(pydantic_object=RequirementList)
        self.input_length = 0  # Initialize input_length in the constructor

    # def parse_input(self, block: CodeBlock) -> str:
    #     text = super().parse_input(block)
    #     self.block_name = str(block.name)
    #     json_input = json.loads(text)

    #     if 'requirements' in json_input and isinstance(json_input['requirements'], list):
    #         input_length = len(json_input['requirements'])  # Count the number of requirements in input
    #         self.input_length = input_length  # Set the input length
    #         print(f"Input length: {self.input_length}")
    #     else:
    #         print("Couldn't find requirements.")
    #     return text

    # def parse_combined_output(self, text: str) -> str:
    #     """Parse the output text from the LLM when multiple inputs are combined."""
    #     json_output = json.loads(text)
    #     output_length: int = 0 

    #     if 'requirements' in json_output and isinstance(json_output['requirements'], list):
    #         output_length = len(json_output['requirements'])  # Count the number of requirements returned in output
    #         print(f"Output length: {output_length}")

    #         # Access the input_length directly
    #         input_length = self.input_length  # Retrieve the input length
    #         print(f"Input length (from parse_input): {input_length}")  
    #         # Compare input length and output length
    #     #     if output_length != input_length:
    #     #         log.debug(f"Array sizes of input and output do not match You must evaluate and return all of the original requirements:\n{text}")
    #     #         raise OutputParserException(f"The input requirements array of size ({input_length}) and output requirements array of size ({output_length}) do not match. You must evaluate and return all of the original requirements")
    #     return text

    def parse(self, text: str):
        output_length: int = 0 

        log.info("Parsing text...")
        if isinstance(text, AIMessage):
            text = text.content
        text = text.lstrip("```json")  # change this to a regex or check for json in the front
        text = text.rstrip("`")
        try:
            obj = parse_json_markdown(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        if not isinstance(obj, dict):
            raise OutputParserException(
                f"Got invalid return object. Expected a dictionary, but got {type(obj)}"
            )
        
        # if 'requirements' in obj and isinstance(obj['requirements'], list):
        #     output_length = len(obj['requirements'])  # Count the number of requirements returned in output
        #     print(f"Output length: {output_length}")

        # input_length = self.input_length  # Retrieve the input length
        # if output_length != input_length:
        #     log.debug(f"Array sizes of input and output do not match You must evaluate and return all of the original requirements:\n{text}")
        #     log.info("The input requirements array of size ({input_length}) and output requirements array of size ({output_length})")
        #     raise OutputParserException(f"The input requirements array of size ({input_length}) and output requirements array of size ({output_length}) do not match. You must evaluate and return all of the original requirements. Using the above evaluated requirements continue generating response for the rest of the requirements in the input array. ")
       
        # move the check into this method 
        return json.dumps(obj)
    

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser."""
        return (
            "Output must contain all original requirements specifications "
            "in a JSON-formatted string. For each and every requirement there should be evaluated criteria C1-C9 each including: "
            "1) The LLM reasoning behind the score. "
            "2) The 'Score' of either a 'pass' or 'fail'."
            "Continue generating your response until all requirements have been returned. "
        )
