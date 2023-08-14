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

temperature = 1
dir_name= "C:\\Users\\cdiggs\\janus\\requirements_evaluation\\"
file_name = 'PSSSUTIL'
suffix = '.txt'
path = os.path.join(dir_name, file_name + suffix)
eval_version = 1

mumps_file = open(path)
mumps_code = mumps_file.read()

#print(mumps_code)

llm = LLM.OpenAI("gpt-3.5-turbo-16k", openai_key, openai_org, temperature=temperature)

# Used to generate the intial prompt fed in for 100 trials, commented to retain integrity across experiments
'''
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
                "Be brief in your requirements doccumentation where possible."
                f"Here is the code {mumps_code}"
            ),
    },
]

output = llm.get_output(prompt)
#print(output[0])
with open(dir_name + file_name + '_Output_' + str(eval_version) + suffix, "w") as text_file:
    text_file.write(output[0])

'''
# Initialize Trials Variables
version = 0
trials = 100 - version

# Load in Requirement for evaluation
dir_name= "C:\\Users\\cdiggs\\janus\\requirements_evaluation\\"
req_name = file_name + '_Output_1'
req_path = os.path.join(dir_name, req_name + suffix)
req_file = open(req_path)
req_text = req_file.read()

for _ in range(trials):
    version += 1
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
                "For each metric,follow these guidelines when generating a score:"
                    "1 = Clear lack of understanding or total failure to address prompt"
                    "2 = Multiple significant errors identified"
                    "3 = 1 significant error or 4-6 minor errors identified"
                    "4 = 1-3 minor errors identified"
                    "5 = No errors identified"
                "Provide a score from 0-5 for each of the 4 metrics listed above, using this rubric."
                "You can use a decimal point to assign a .5 score between whole numbers if the evaluation in between two categories."
            ),
        },
        {
            "role": "user",
            "content": (
                    "Please evaluate the following requriments doccumentation, providing a number between 0-5 for each metric."
                    f"Here is the requirements doccumentation {req_text}"
                    "Use this exact format for your evaulation:"
                    "Performance - <insert score here>"
                    "Explainability - <insert score here>"
                    "Calibration - <insert score here>"
                    "Faithfulness - <insert score here>"
                    "For reference when creating your evalaution, use the source code that the requirements were created using."
                    f"Here is the code {mumps_code}"
                ),
        },
    ]

    eval = llm.get_output(eval_prompt)
    #print(output[0])
    with open("C:\\Users\\cdiggs\\janus\\requirements_evaluation\\Fixed Req Variable Temp\\" + str(temperature) + "_" + file_name + "_evaluations\\" + file_name + '_Evaluation_' + str(version) + suffix, "w") as text_file:
        text_file.write(eval[0])
    print(f"Completed Version: {version}")

