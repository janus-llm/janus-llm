import argparse

from janus.parsers.code_parser import PARSER_TYPES
from janus.prompts.prompt import JANUS_PROMPT_TEMPLATES_DIR
from janus.translate import VALID_MODELS, Translator
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

AVAILABLE_PROMPTS = [d.name for d in JANUS_PROMPT_TEMPLATES_DIR.iterdir() if d.is_dir()]

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
    "--source-lang",
    type=str,
    choices=LANGUAGES.keys(),
    required=True,
    help="The language of the source code",
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
    "--target-lang",
    type=str,
    default="python-3.10",
    help=(
        "The desired output language to translate the source code to. "
        "The format can follow a 'language-version' syntax. "
        "Use 'text' to get plaintext results as returned by the LLM. "
        "Examples: python-3.10, mumps, java-10, text"
    ),
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="translated",
    help="The directory to store the translated code in",
)
parser.add_argument(
    "--llm-name",
    type=str,
    choices=VALID_MODELS,
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
    action="store_true",
    help="Whether to overwrite existing files in the output directory",
)
parser.add_argument(
    "--temp",
    type=float,
    default=0.7,
    help="Sampling temperature.",
)
parser.add_argument(
    "--prompt-template",
    type=str,
    choices=AVAILABLE_PROMPTS,
    default="simple",
    help=(
        "Name of the Janus prompt template directory or "
        "path to a directory containing those template files."
    ),
)
parser.add_argument(
    "--parser-type",
    type=str,
    choices=PARSER_TYPES,
    default="code",
    help=("The type of parser to use"),
)

if __name__ == "__main__":
    args = parser.parse_args()
    try:
        target_language, target_version = args.target_lang.split("-")
    except ValueError:
        target_language = args.target_lang
        target_version = None
    # make sure not overwriting input
    if (
        args.source_lang.lower() == target_language.lower()
        and args.input_dir == args.output_dir
    ):
        log.error("Output files would overwrite input! Aborting...")
        exit(-1)

    model_arguments = dict(temperature=args.temp)
    translator = Translator(
        model=args.llm_name,
        model_arguments=model_arguments,
        source_language=args.source_lang,
        target_language=target_language,
        target_version=target_version,
        max_prompts=args.max_prompts,
        prompt_template=args.prompt_template,
        parser_type=args.parser_type,
    )
    translator.translate(args.input_dir, args.output_dir, args.overwrite)
