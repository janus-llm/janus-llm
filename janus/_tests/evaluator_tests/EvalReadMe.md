

# LLM Self Eval 

The `llm-self-eval` command leverages the converter class to perform evaluations on generated outputs from large language models. 

The input directory structure will be maintained in the output evaluations. The input files should contain an array of items to be evaluated. Each item will be evaluated individually based off of the corresponding prompt. Set evaluations can be performed as well but please note that each file to be evaluated must contain only one array with the items to be evaluated. 


## Evaluation Types 

| Evaluation Type | Status | Command |
| ----------- | ----------- | ----------- |
| Incose  | In progress | ```-e "incose"```
| Incose sets  | TODO | n/a 
| Seedling comments   | TODO | n/a
| Seedling comment sets  | TODO | n/a 

## How to Run 

Structure: 
```
janus llm-self-eval -i {path/to/input/files} -l json -o {path/to/output/files} -e {evaluator_type} -rc {# of items to evaluate at a time}

```
| Flag | Meaning | Example |
| ----------- | ----------- | ----------- |
| `-i`  | Input Directory | ```"path/to/input/files"```
| `-o`  | Output Directory | ```"path/to/output/files"```
| `-l` | Evaluation language | `json` 
| `-e`  | Evaluation Type | ```"incose"```
| `-rc`  | Number of lines to evaluate at a time (rec 5-10) | `5` 

 Example test command:
```
janus llm-self-eval -i _tests/incose_tests/input/ -l json -o testOutput/ -e "incose" -rc 5
```

## Adding an Evaluation Type 
#### 1. Create a Parser 

- In ```janus/parsers/eval_parsers``` 
  - See `janus/janus/parsers/eval_parsers/incose_parser.py` for reference

#### 2. Create a the Prompt

 - In ```janus/prompts/eval_prompts```
 - Create a new directory with the name of your evaluation type. **Note: The name that you use is how you will call the evaluation type eg** ```-e "incose"```
 - `human.txt`  - this is the main prompt that contains the scoring rubric and the commands for the llm to follow 
 - `system.txt`  - the initial instructions for the evaluating llm 
- `variables.json`  - contains the structure for what the returned evaluation should look like 

#### 3. Update ```evaluate.py```
1. Import your new parser
2. Append if statment with your new parser
   ```
   # Setting parser type here
        if evaluation_type == "incose":
            self._parser = IncoseParser()
        if evaluation_type == {your_new_evaluation_type}
            self._parser = {YourImportedParser()}}
    ```

## Example Inputs
```
{
    "code": "DFHEISTG DSECT\nAPPLID   DS    CL08               CICS Applid\nSYSID    DS    CL04               CICS SYSID\n*\n***********************************************************************\n* Dynamic Storage Area (End)                                          *\n***********************************************************************\n*\n***********************************************************************\n* DFHCOMMAREA                                                         *\n***********************************************************************\n*",
    "requirements": [
        "981273129",
        "Testing for the CACBAR constant shall verify that it is recognized by the software as indicating the beginning of a DFHCOMMAREA and that it has been assigned a numeric value of 12 and that it is secure and that it is understandable and the testing must have 100% coverage and it must return useful content to a mixed audience.",
        "The MS_WAIT field shall be a fullword integer (4 bytes) designed to store a wait time ranging from 1 millisecond to 900 milliseconds.",
        "The software shall consider the DFHEISTG data structure as the end of a dynamic storage area.",
        "The software shall recognize a constant named CACBAR, which is equivalent to the numeric value 12, indicating the beginning of a DFHCOMMAREA from the requesting program.",
        "Hi there!",
        "Limitations: The provided code snippet does not specify operations or methods for interacting with the DFHEISTG data structure or the DFHCOMMAREA. The functionality related to these structures must be defined in additional requirements or specifications not provided in the code snippet.",
        "Testing of the DFHEISTG structure shall verify that the STIMERID field can store a 4-byte character string and that the MS_WAIT field can store an integer value within the range of 1 to 900. Additionally, testing should confirm that these fields are part of the defined dynamic storage area.",
        "Testing for the CACBAR constant shall verify that it is recognized by the software as indicating the beginning of a DFHCOMMAREA and that it has been assigned a numeric value of 12.",
        "The software requirements specification document must acknowledge areas where the code's functionality is not completely specified, such as the absence of detailed operations for the DFHEISTG structure or the contents and structure of the DFHCOMMAREA, and note these as areas for further clarification.",
        "781",
        "It worked!"
    ]
}

