from janus.converter.converter import Converter
from janus.language.combine import JsonCombiner
from janus.parsers.eval_parser import EvaluationParser
from janus.utils.logger import create_logger
from pathlib import Path
import os

log = create_logger(__name__)

class Evaluator(Converter):
    """Evaluator

    A class that performs an LLM self evaluation on an input target, with an associated prompt.
    """
    def __init__(
        self,
        # multi_prompt_dir = None,
        # prompt = None,  
         **kwargs)->None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(**kwargs)
        self.set_prompt("evaluate")
        self._combiner = JsonCombiner()
        self._parser = EvaluationParser()
        self._load_parameters()
        # self.multi_prompt_dir = multi_prompt_dir

    def _self_test(self, multi_prompt_dir: Path, in_path: Path,  out_path: Path, prompt: Path) -> None:
        print("Prompt path: ",  out_path)
        print("Input path: ",  in_path)
        
        if multi_prompt_dir is not None: 
            print("Multiprompt path: ",  multi_prompt_dir)
            # read_prompt_files(multi_prompt_dir)
        if prompt is Path:
            print("Single prompt: ",  prompt)
        # else:
        #     raise ValueError(
        #             f"Prompt direcotry or file not given. \n"
        #             f"Please specify evaluation prompt path using -MP or -P flag."
        #         )
        return
    
    def read_prompt_files(self):
        """Reads in a directory of prompts and parses out the name and the prompt content and stores in an object. 

        Arguments:
            directory_path: Path to direcotry of multiple txt files containing prompts
        
        Return:
            An array of objects with prompt name (file name) and the prompt (file content)
        """
        directory_path = self.multi_prompt_dir
        multi_prompt_data = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                # Get the file name without extension
                file_name_without_extension = os.path.splitext(filename)[0]
                # Get the full file path
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r') as file:
                    content = file.read()
                # Create a dictionary object with file name and content
                file_data = {
                    "prompt_name": file_name_without_extension,
                    "prompt": content
                }
                multi_prompt_data.append(file_data)

        # Print the list of file data objects
        # for data in multi_prompt_data:
        #     print(data['prompt_name'])
        #     print(data['prompt'])
        return multi_prompt_data