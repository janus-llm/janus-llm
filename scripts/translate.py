import argparse

from janus.translate import Translator
from janus.utils.logger import create_logger

log = create_logger(__name__)

parser = argparse.ArgumentParser(
    prog="Janus",
    description=(
        "Translate code from one language to another "
        "using LLMs! This will require an OpenAI "
        "API key. Set the OPENAI_API_KEY "
        "environment variable to your key"
    ),
)
parser.add_argument(
    "--input-lang", type=str, required=True, help="The language of the source code"
)
parser.add_argument(
    "--input-dir",
    type=str,
    required=True,
    help=(
        "The directory containing the source code to be translated. "
        "The files should all be in one flat directory"
    ),
)
parser.add_argument(
    "--output-lang",
    type=str,
    required=True,
    help=(
        "The desired output language to translate the source code to. "
        "The format should follow a 'language-version' syntax. "
        "Example: python-3.10, java-10, etc."
    ),
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="/tmp/translated",
    help="The directory to store the translated code in",
)
parser.add_argument(
    "--llm-name",
    type=str,
    default="gpt-3.5-turbo",
    help=(
        "The OpenAI model name to use. See this link for more details:\n"
        "https://platform.openai.com/docs/models/overview"
    ),
)
parser.add_argument(
    "--max-prompts",
    type=int,
    default=10,
    help=(
        "The maximum number of times to prompt a model on one functional block "
        "before exiting the application. This is to prevent wasting too much money."
    ),
)
parser.add_argument(
    "--overwrite",
    action='store_true',
    help="Whether to overwrite existing files in the output directory",
)

if __name__ == "__main__":
    args = parser.parse_args()
    output_lang_name, output_lang_version = args.output_lang.split("-")
    translator = Translator(
        args.llm_name,
        args.input_lang,
        output_lang_name,
        output_lang_version,
        args.max_prompts,
    )
    translator.translate(args.input_dir, args.output_dir, args.overwrite)
