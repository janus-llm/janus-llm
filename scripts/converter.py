import subprocess
from typing import Tuple
from janus.llm import LLM
from janus.utils.logger import create_logger
import re
import os


log = create_logger(__name__)

openai_key = os.getenv("OPENAI_API_KEY")
openai_org = os.getenv("OPENAI_ORG")

def query_fortran_script(file_name):
    with open(file_name, "r") as file:
        fortran_code = file.read()

    print(fortran_code)

    llm = LLM('gpt-3.5-turbo', openai_key, openai_org)

    prompt = [
        {
            "role": "system",
            "content": "Your purpose is to convert Fortran f90 file code into runnable Python code (python version 3.9)"
        },
        {
            "role": "user",
            "content": f"Please convert the following Fortan f90 code which is in string format into usuable python code.  Please encapsulate the code into a main function and use __main__.  Here is the code {fortran_code}.  For any variable that is defined out side of that function please explain that variable"
        }
    ]
    
    output = llm.get_output(prompt)
    try:
        # response = re.findall(r"\{.*?\}", output)[0].strip("{}")
        pattern = r"```(.*?)```"
        response = re.search(pattern, output, re.DOTALL)
        response = response.group(1).strip('python\n')
    except Exception:
        log.warning(f"Could not find code in output:\n\n{output}")
    res =  parse_gpt_python_input(response)

    while res[0] == True:
        val = input('Statement encountered an error, continue? 1: yes, 2: no\n')
        if (val == str(1) or val == 'no'):
            res[0] = False
            continue


        # Requery ChatGPT to fix its life mistakes
        prompt = [
            {
                "role": "system",
                "content": "Your purpose is to convert Fortran f90 file code into runnable Python code (python version 3.9) and you messed up the output of your last query"
            },
            {
                "role": "user",
                "content": f"From this original code we gave you seen here {fortran_code} it returned the following error {res[1]}.  Please fix this."
            }
        ]
        
        output = llm.get_output(prompt)
        try:
            response = re.findall(r"\{.*?\}", output)[0].strip("{}")
        except Exception:
            log.warning(f"Could not find prompt in output:\n\n{output}")
        res =  parse_gpt_python_input(response)

    

      
    
def parse_gpt_python_input(python_script) -> Tuple[bool, str]:
    print(python_script)

    # Write the script to a file
    with open('temp_script.py', 'w') as script_file:
        script_file.write(python_script)


    error_code = False
    # Run the script and capture the output or error
    try:
        result = subprocess.check_output(['python', 'temp_script.py'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as error:
        error_code = True;
        result = error.output

    # Remove the temporary script file
    subprocess.run(['rm', 'temp_script.py'])

    # Print the output or error
    print(result)
    if error_code:
        return True, result
    
    with open('final_script.py', 'w') as script_file:
        script_file.write(python_script)
    return False, result

def main():

    file_name = 'elmfire_centroidfcn.f90'
    query_fortran_script(file_name)
    # python_script = test_python_script2
    # out = parse_gpt_python_input(python_script)
    # print(out[1])

if __name__ == "__main__":
    main()