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
temperatures = [i / 10 for i in range(0, 11)]

kwargs = dict(
    model="gpt-3.5-turbo-16k",
    source_language="mumps",
    target_language="python",
    target_version="3.10",
    max_prompts=10,
    prompt_template="simple",
    maximize_block_length=False,
    force_split=False,
)

for i in range(iterations):
    log.info(f"Iteration {i}")
    for temperature in temperatures:
        log.info(f"Temperature {temperature}")
        translator = Translator(model_arguments=dict(temperature=temperature), **kwargs)
        outdir = output_dir / "model_temperature" / f"gpt-4_{temperature}" / f"{i}"
        outdir.mkdir(parents=True, exist_ok=True)
        translator.translate(input_dir, outdir, overwrite=False)
