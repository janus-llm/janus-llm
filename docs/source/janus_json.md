# Janus JSON Files

Janus JSON files are both created at the output of many of the `janus` CLI commands as well as able to be used as input for the same commands.

## Explanation

The Janus JSON file is a standardized input/output format for the `janus` CLI tool. It contains the following fields:

```json
{
  "metadata": {
    "translation_complete": bool,
    "language": str,
    "model_name": OPTIONAL[str],
    "cost": OPTIONAL[float],
    "processing_time": OPTIONAL[float],
    "request_input_tokens": OPTIONAL[int],
    "request_output_tokens": OPTIONAL[int],
    "num_requests": OPTIONAL[int],
    "input_tokens": OPTIONAL[int],
    "output_tokens": int,
    "start_line": int,
    "start_char": int,
    "start_byte": int,
    "end_line": int,
    "end_char": int,
    "end_byte": int,
    "hash": int
  },
  "output": OPTIONAL[str],
  "outputs": [
    <Janus JSON>,
    ...,
    <Janus JSON>
  ],
  "input": str | <Janus JSON>
}
```

### Keys

- `input`: The input to the command. This is usually the source code or whatever the command is processing. When the output is from a pipeline, this will be the Janus JSON object associated with the input to this stage in the pipeline.
- `output`: A string containing the output of the converter. If the output is composed of multiple pieces (e.g. the input was chunked and the `combine_output` option of the Converter is disabled), this field does not exist.
- `outputs`: A list of Janus JSON objects containing the outputs of the converter. If the converter produced only one output (i.e. the `output` field is populated), this may be an empty list.
- `metadata`: A dictionary containing metadata about the command. This includes:
  - `translation_complete`: A True or False value indicating whether the translation of this object was successful.
  - `language`: The language of the content of the `output` or `outputs` fields (usually either a programming language or "json").
  - `model_name`: The name of the language model used to complete the conversion.
  - `cost`: The cost of the command in USD.
  - `processing_time`: The time it took to process the command in seconds.
  - `request_input_tokens`: The total number of tokens sent to the LLM as input, including retries and refinement.
  - `request_output_tokens`": The total number of tokens recieved from the LLM as output, including retries and refinement.
  - `num_requests`: The number of requests made to the LLM. If there are multiple requests, for a single [pipeline](pipelines.md) stage, then this likely means there there was a failure in the pipeline and the stage was retried.
  - `input_tokens`: The number of input tokens in the request to to the LLM, including prompt tokens.
  - `output_tokens`: The number of tokens in the final output.
  - `start_line`: The index of the first line of input to this step in the pipeline. Indexes into the contents of `input`.
  - `start_char`: The index of the first character in the first line of input to this step in the pipeline. Indexes into the contents of `input`.
  - `start_byte`: The index of the first byte of input to this step in the pipeline. Indexes into the contents of `input`.
  - `end_line`: The index of the last line of input to this step in the pipeline. Indexes into the contents of `input`.
  - `end_char`: The index of the last character in the last line of input to this step in the pipeline. Indexes into the contents of `input`.
  - `end_byte`: The index of the last byte of input to this step in the pipeline. Indexes into the contents of `input`.
  - `hash`: A unique hash for this output. Can be used to identify common ancestors of downstream representations.


## Example

An example Janus JSON file is shown below. The command used to create this JSON file is here:

```bash
janus translate \
    --input janus/cli \
    --source-language python \
    --output test-out/js \
    --target-language javascript \
    --llm mchat \
    --splitter ast-flex
```

```json
{
  "metadata": {
    "converter_name": "Translator",
    "translation_complete": true,
    "language": "javascript",
    "model_name": "mchat",
    "cost": 0.010664499999999999,
    "processing_time": 15.649877786636353,
    "request_input_tokens": 1578,
    "request_output_tokens": 575,
    "num_requests": 1,
    "input_tokens": 1421,
    "output_tokens": 570,
    "start_line": 0,
    "start_char": 0,
    "start_byte": 0,
    "end_line": 77,
    "end_char": 1,
    "end_byte": 2269,
    "hash": -5796694790857239083
  },
  "output": "import { Path } from \"pathlib\" <...>\n  await translator.translate(inputDir, outputDir, failureDir, overwrite, collection);\n}\n",
  "outputs": [],
  "input": {
    "metadata": {
      "translation_complete": false,
      "language": "python",
      "output_tokens": 1421,
      "start_line": 0,
      "start_char": 0,
      "start_byte": 0,
      "end_line": 226,
      "end_char": 83,
      "end_byte": 6624,
      "hash": 6184682770588683329
    },
    "output": "from pathlib import Path <...>\n    translator.translate(input_dir, output_dir, failure_dir, overwrite, collection)\n",
    "outputs": [],
    "input": "from pathlib import Path <...>\n    translator.translate(input_dir, output_dir, failure_dir, overwrite, collection)\n"
  }
}
```

To use this same file as an input for a `janus translate` command that translates the code from JavaScript back to Python, you would run the following command:

```bash
janus translate \
    --input test-out/js \
    --source-language javascript \
    --output test-out/py \
    --target-language python \
    --llm mchat \
    --splitter ast-flex \
    --use-janus-inputs
```

The key difference here is the `--use-janus-inputs` flag, which tells Janus to use the Janus JSON files as input instead of the source code files.

The resultant JSON file is shown below:

```json
{
  "metadata": {
    "converter_name": "Translator",
    "translation_complete": true,
    "language": "python",
    "model_name": "mchat",
    "cost": 0.00774125,
    "processing_time": 6.3030149936676025,
    "request_input_tokens": 731,
    "request_output_tokens": 521,
    "num_requests": 1,
    "input_tokens": 570,
    "output_tokens": 516,
    "start_line": 0,
    "start_char": 0,
    "start_byte": 0,
    "end_line": 71,
    "end_char": 89,
    "end_byte": 2291,
    "hash": 6023821945816684597
  },
  "output": "from pathlib import Path <...>\n    await translator.translate(input_dir, output_dir, failure_dir, overwrite, collection)",
  "outputs": [],
  "input": {
    "metadata": {
      "converter_name": "Translator",
      "translation_complete": true,
      "language": "javascript",
      "model_name": "mchat",
      "cost": 0.010664499999999999,
      "processing_time": 15.649877786636353,
      "request_input_tokens": 1578,
      "request_output_tokens": 575,
      "num_requests": 1,
      "input_tokens": 1421,
      "output_tokens": 570,
      "start_line": 0,
      "start_char": 0,
      "start_byte": 0,
      "end_line": 77,
      "end_char": 1,
      "end_byte": 2269,
      "hash": -6931968753527424146
    },
    "output": "import { Path } from \"pathlib\"; <...>\n  await translator.translate(inputDir, outputDir, failureDir, overwrite, collection);\n}\n",
    "outputs": [],
    "input": {
      "metadata": {
        "translation_complete": false,
        "language": "python",
        "output_tokens": 1421,
        "start_line": 0,
        "start_char": 0,
        "start_byte": 0,
        "end_line": 226,
        "end_char": 83,
        "end_byte": 6624,
        "hash": 6184682770588683329
      },
      "output": "from pathlib import Path <...>\n    translator.translate(input_dir, output_dir, failure_dir, overwrite, collection)\n",
      "outputs": [],
      "input": "from pathlib import Path <...>\n    translator.translate(input_dir, output_dir, failure_dir, overwrite, collection)\n"
    }
  }
}
```
