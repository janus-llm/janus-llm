import os
import re
import subprocess
import pypandoc
from typing import Tuple

from janus.llm import openai as LLM
#from janus.utils.logger import create_logger

from decouple import config   

openai_key = config("OPENAI_API_KEY")
openai_org = config("OPENAI_ORG")

dir_name= "C:\\Users\\cdiggs\\janus\\mumps_tests\\"
file_name = 'PSSTXT'
suffix = '.m'
version = 'V1'
path = os.path.join(dir_name, file_name + suffix)

mumps_file = open(path)
mumps_code = mumps_file.read()
#print(mumps_code)

llm = LLM.OpenAI("gpt-3.5-turbo", openai_key, openai_org, temperature=0.5)

prompt = [
    {
        "role": "system",
        "content": (
            "Your purpose is to convert a txt file that contains MUMPS code into a set of strict software requirements, for an application written in python code."
            "You will convert MUMPS code into a series of IEEE SRS requirements, using only system shall statements in a numbered list."
            "Focus on a detailed explanation of the codes purpose, functionality, and the necessary components required to reproduce this functionality in an EHR."
            "Describe the functions, variables, and define the inputs and outputs for the code segment."
            "Identify dependencies in the code external to the file. Be clear about where those sub-functions are and what other functions are required."
            "Only use concise plain language. Never output MUMPS code in the requirements documentation."
        ),
    },
    {
        "role": "user",
        "content": (
                "Please convert the following mumps code which is in a .txt file format into requriments that can replicate its functionality in python."
                "This MUMPS code is a billing drug count checker."
                "If you think any section of the MUMPS code is difficult for an M programmer understand, state that in the doccument."
                f"Here is the code {mumps_code}"
            ),
    },
]

output = llm.get_output(prompt)
#print(output[0])
with open(file_name + '_Output_' + version, "w") as text_file:
    text_file.write(output[0])

eval_prompt = [
    {
        "role": "system",
        "content": (
            "Your purpose is to review a file that contains a set of strict software requirements, for an application written in python code."
            "You will examine the contents of the source code written in MUMPS, and the requirements extracted from it and evaluate it using 4 metrics."
            "1. Performance - Provide an overall evalutation of the quality of the requirements, and how well they match the source code."
            "2. Explainability - Provide an evalaution of how clearly the requirements are explained, and how easy they are to follow"
            "3. Calibration - Identify any logical inconsistencies, or duplicated requirements."
            "4. Faithfulness - Identify if any requirements are generalized, or not explicitly related to the source code."
            "Only use concise plain language. Provide a score from 0-5 for each of the 4 metrics listed above."
            "Explain your evalaution in a few short sentences, using examples when appropriate. If a specific requirements caused you to dock points, list it."
        ),
    },
    {
        "role": "user",
        "content": (
                "Please evaluate the following requriments doccuemntation as a technical SRS analyst"
                f"Here is the requirements doccumentation {output[0]}"
                "For reference when creating your evalaution, use the source code that the requirements were created using."
                f"Here is the code {mumps_code}"
            ),
    },
]

eval = llm.get_output(eval_prompt)
#print(output[0])
with open(file_name + '_Evalaution_' + version, "w") as text_file:
    text_file.write(eval[0])

