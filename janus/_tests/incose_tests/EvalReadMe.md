# LLM Self Eval 

WIP - will need to finish and move to appropriate spot 

## Evaluation Types 


| Evaluation Type | Status | Command |
| ----------- | ----------- | ----------- |
| Incose  | In progress | ```-e "incose"```
| Incose sets  | TODO | n/a 
| Seedling comments   | TODO | n/a
| Seedling comment sets  | TODO | n/a 

## How to Run 

``` 
// Test run: 
janus llm-self-eval -i _tests/incose_tests/input/ -l json -o testOutput/ -e "incose"
```

## Adding an Evaluation Type 
#### 1. Create a Parser 

- In ```janus/parsers/eval_parsers``` 

#### 2. Create a the Prompt

 - In ```janus/prompts/eval_prompts```
 - Create a new direcotry with the name of your evalution type. **Note: The name that you use is how you will call the evaluation type eg** ```-e "incose"```

#### 3. Update ```evaluate.py```

