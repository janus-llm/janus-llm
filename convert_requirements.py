import os
import re
import subprocess
import pypandoc
from typing import Tuple

from janus.llm import openai as LLM
from janus.utils.logger import create_logger

from decouple import config   

openai_key = config("OPENAI_API_KEY")
openai_org = config("OPENAI_ORG")

dir_name= "C:\\Users\\cdiggs\\janus\\mumps_tests\\"
file_name = 'PSS54'
suffix = '.txt'
path = os.path.join(dir_name, file_name + suffix)

mumps_file = open(path)
mumps_code = mumps_file.read()
#print(mumps_code)

llm = LLM.OpenAI("gpt-3.5-turbo", openai_key, openai_org, temperature=0)

prompt = [
    {
        "role": "system",
        "content": (
            "Your purpose is to convert a txt file that contains MUMPS code into a set of strict software requirements, for an application written in python code."
            "You will convert MUMPS code into a series of IEEE SRS requirements, using system shall statements in a numbered list."
            "Focus on a detailed explanation of the codes purpose, functionality, and the necessary components required to reproduce this functionality in an EHR."
            "Describe the functions, variables, and define the inputs and outputs for the code segment."
            "Identify dependencies in the code external to the file. Be clear about where those dependencies are and what other functions are required."
            "Only use concise plain language. Never output MUMPS code in the requirements documentation."
        ),
    },
    {
        "role": "user",
        "content": (
                "Please convert the following mumps code which is in a .txt file format into requriments that can replicate its functionality in python."
                "This MUMPS code is an API for information from file 54."
                "If you think any section of the MUMPS code is difficult to understand, state that in the doccument."
                f"Here is the code {mumps_code}"
            ),
    },
]

output = llm.get_output(prompt)
#print(output[0])
with open(file_name + '_Output V7', "w") as text_file:
    text_file.write(output[0])
