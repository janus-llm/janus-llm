import tiktoken
from pathlib import Path
import argparse
from typing import Dict
import numpy as np
import scipy


COST_PER_MODEL: Dict[str, Dict[str, float]] = {
    "gpt-4": {"input": 0.00003, "output": 0.00006},
    "gpt-4-32k": {"input": 0.0006, "output": 0.00012},
    "gpt-3.5-turbo": {"input": 0.0000015, "output": 0.000002},
    "gpt-3.5-turbo-16k": {"input": 0.000003, "output": 0.000004},
}


parser = argparse.ArgumentParser(
    prog="Estimate OpenAI Costs",
    description=(
        "Estimate OpenAI API request costs based on model, system prompt, and "
        "example input/output messages"
    ),
)

parser.add_argument(
    "--model",
    type=str,
    nargs="?",
    choices=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
    default="gpt-3.5-turbo-16k",
    const="gpt-3.5-turbo-16k",
    help="The model in use.",
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--system-prompt",
    type=str,
    default=None,
    help="The system prompt. If no system prompt is provided, will use OpenAI's "
    "default prompt.",
)
group.add_argument(
    "--system-prompt-file",
    type=str,
    default=None,
    help="A text file containing the system prompt. Incompatible with "
    "--system-prompt argument.",
)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--example-input",
    type=str,
    default=None,
    help="An example input. If the input changes with each request, use the "
    "--example-input-dir argument.",
)
group.add_argument(
    "--example-input-dir",
    type=str,
    default=None,
    help="A path to a flat directory containing example input text files. "
    "Incompatible with --example-input.",
)

parser.add_argument(
    "--example-output-dir",
    type=str,
    required=True,
    help="A path to a flat directory containing example output text files.",
)

parser.add_argument(
    "-n",
    type=int,
    default=None,
    help="The number of requests you expect to make. By default, this is the "
    "number of output files in the directory provided in the "
    "--example-output-dir argument",
)

args = parser.parse_args()

encoding = tiktoken.encoding_for_model(args.model)
if args.system_prompt:
    system_length = len(encoding.encode(args.system_prompt))
elif args.system_prompt_file:
    system_length = len(encoding.encode(Path(args.system_prompt_file).read_text()))
else:
    system_length = len(encoding.encode("You are a helpful assistant"))

if args.example_input:
    input_length_mean = len(encoding.encode(args.example_input))
    input_length_low = input_length_mean
    input_length_high = input_length_mean
else:
    inputs = [p.read_text() for p in Path(args.example_input_dir).glob("*.txt")]
    input_lengths = np.array([len(encoding.encode(p)) for p in inputs])
    input_length_mean = input_lengths.mean()
    input_length_low, input_length_high = scipy.stats.t.interval(
        confidence=0.95,
        df=len(input_lengths) - 1,
        loc=input_length_mean,
        scale=scipy.stats.sem(input_lengths),
    )

outputs = [p.read_text() for p in Path(args.example_output_dir).glob("*.txt")]
output_lengths = np.array([len(encoding.encode(p)) for p in outputs])
output_length_mean = output_lengths.mean()
output_length_low, output_length_high = scipy.stats.t.interval(
    confidence=0.95,
    df=len(output_lengths) - 1,
    loc=output_length_mean,
    scale=scipy.stats.sem(output_lengths),
)

n_outs = len(output_lengths)
if args.n:
    n_outs = args.n

total_length_mean = system_length + input_length_mean + output_length_mean

system_cost = COST_PER_MODEL[args.model]["input"] * system_length
total_cost_mean = (
    system_cost
    + COST_PER_MODEL[args.model]["input"] * input_length_mean
    + COST_PER_MODEL[args.model]["output"] * output_length_mean
)
low_price = (
    system_cost
    + COST_PER_MODEL[args.model]["input"] * input_length_low
    + COST_PER_MODEL[args.model]["output"] * output_length_low
)
high_price = (
    system_cost
    + COST_PER_MODEL[args.model]["input"] * input_length_high
    + COST_PER_MODEL[args.model]["output"] * output_length_high
)

print(
    f"""
System prompt tokens:    {system_length:,d}
Mean user prompt tokens  {input_length_mean:,.2f}
Mean output tokens       {output_length_mean:,.2f}
Mean tokens per request: {total_length_mean:,.2f}
Mean price per request:  ${total_cost_mean:,.2f}
    95% confidence:      ${low_price:,.2f} - ${high_price:,.2f}
Expected total cost:     ${total_cost_mean*n_outs:,.2f}
    95% confidence:      ${low_price*n_outs:,.2f} - ${high_price*n_outs:,.2f}
"""
)
