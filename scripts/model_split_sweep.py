from pathlib import Path
import argparse
from janus.translate import Translator
from janus.utils.logger import create_logger

log = create_logger(__name__)

parser = argparse.ArgumentParser(
    prog="Run Comparative Tests",
    description=(
        "Run comparative tests on the supplied directory. "
        "This will require an OpenAI API key. Set the OPENAI_API_KEY "
        "environment variable to your key"
    ),
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
    "--output-dir",
    type=str,
    default="/tmp/translated",
    help="The directory to store the translated code in",
)

args = parser.parse_args()
input_dir = args.input_dir
output_dir = Path(args.output_dir)

iterations = 10
models = [
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-16k',
    'gpt-4'
]

kwargs = dict(
    model_arguments=dict(temperature=0.7),
    source_language='mumps',
    target_language='python',
    target_version='3.10',
    max_prompts=10,
    prompt_template='simple',
)

for i in range(iterations):
    for model in models:
        translator = Translator(
            model=model,
            maximize_block_length=True,
            force_split=False,
            **kwargs
        )
        outdir = output_dir / f"{model}_nosplit" / str(i)
        outdir.mkdir(parents=True, exist_ok=True)
        translator.translate(input_dir, outdir, overwrite=False)

        translator = Translator(
            model=model,
            maximize_block_length=False,
            force_split=True,
            **kwargs
        )
        outdir : Path = output_dir / f"{model}_split" / str(i)
        outdir.mkdir(parents=True, exist_ok=True)
        translator.translate(input_dir, outdir, overwrite=False)
