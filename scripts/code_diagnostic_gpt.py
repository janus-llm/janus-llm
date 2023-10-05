import argparse
import re

import openai
import tiktoken

from janus.llm.openai import TOKEN_LIMITS

parser = argparse.ArgumentParser(
    prog="Syntax Error Counter",
    description=(
        "Use ChatGPT to count the syntax error in Python code. "
        "This requires an OpenAI API key. set the OPENAI_API_KEY "
        "environment variable to your key."
    ),
)
parser.add_argument("filename")
parser.add_argument(
    "--give-example",
    action="store_true",
    help="Whether to provide ChatGPT with example input and output",
)
parser.add_argument(
    "--number-lines", action="store_true", help="Whether to number the lines of code"
)
parser.add_argument(
    "--temp",
    type=float,
    default=0.7,
    help="Temperature. Set to 0 for deterministic output. Default 0.7",
)
parser.add_argument(
    "--model", type=str, default="gpt-3.5-turbo-16k-0613", help="The OpenAI model to use"
)

args = parser.parse_args()
encoding = tiktoken.encoding_for_model(args.model)
token_limit = TOKEN_LIMITS.get(args.model, 4096)

messages = list()

# The system prompt defines the overall behavior of the agent
system_prompt = (
    "Act as a static analysis tool for Python code. Given a sample of Python "
    "(wrapped in triple backticks), identify the syntax errors. Each line of "
    "your response should be numbered, and include the original code wrapped in "
    "backticks, followed by a short (1-2 sentence) description of the issue. "
    "Skip lines that have no syntax errors. Do not include formatting issues or "
    "logical errors, only report syntax errors that would prevent compilation "
    "with a tool like py_compile."
)
input_tokens = len(encoding.encode(system_prompt))
messages.append(dict(role="system", content=system_prompt))

# If indicated, provide example input and output for GPT to emulate
if args.give_example:
    example_input = """
def is_prime(num)
  if num == 1:
    print(num, "is not a prime number"))
  elif num > 1:
  # check for factors
  for i in range(2, num):
    if (num %% i) == 0:
      Return False
      break
    else:
      return true

  # if input number is less than
  # or equal to 1, it is not prime
  else:
    return False

  elif num < 1:
    return False
"""
    example_output = """
1. line 1: `def is_prime(num)`: Missing expected character ':'
2. line 3: `    print(num, "is not a prime number"))`: Unexpected character ')'
3. line 6: `  for i in range(2, num):`: Expected an indented block after 'elif' statement
4. line 7: `       if (num %% i) == 0:`: Invalid operator '%%'
5. line 8: `         Return False`: Invalid keyword 'Return'
6. line 18: `  elif num < 1:`: Unexpected 'elif' with no 'if'
"""
    # Prepend each line with a line number if indicated
    if args.number_lines:
        example_input = "\n".join(
            f"{i + 1}|{line}" for i, line in enumerate(example_input.split("\n"))
        )
    else:
        # Otherwise, remove line numbers in output
        example_output = re.sub(r" line \d+:", "", example_output)

    # Delimit code with backticks
    example_input = f"```{example_input}```"

    # Add to token limit
    input_tokens += len(encoding.encode(example_input))
    input_tokens += len(encoding.encode(example_output))

    # Fudge factor, this will usually only be 6-8 depending on the model
    input_tokens += 10

    # Add to messages list
    messages.extend(
        [
            dict(role="user", content=example_input),
            dict(role="assistant", content=example_output),
        ]
    )

code = open(args.filename, "r").read()

# Prepend each line with a line number if indicated
if args.number_lines:
    code = "\n".join(f"{i+1}|{line}" for i, line in enumerate(code.split("\n")))

code = f"```\n{code}\n```"

input_tokens += len(encoding.encode(code))

# Fudge factor, this will usually only be 6-8 depending on the model
input_tokens += 10

# Add to messages list
messages.append(dict(role="user", content=code))

if __name__ == "__main__":
    response = openai.ChatCompletion.create(
        model=args.model,
        messages=messages,
        stream=True,
        max_tokens=token_limit - input_tokens,
        temperature=args.temp,
    )

    try:
        for resp in response:
            delta = resp.choices[0]["delta"]
            tok = delta.get("content", None)
            if tok is not None:
                print(tok, end="")
    except Exception:
        print()
        raise

    print()
