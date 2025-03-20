import os
from pathlib import Path

import tiktoken
import typer
from rich import print
from typing_extensions import Annotated

tokenizer = typer.Typer(
    help="LLM commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@tokenizer.command(
    "download", help="Download the tokenizers required to run Janus offline."
)
def tokenizer_download(
    directory: Annotated[
        str, typer.Argument(help="The directory to download the tokenizers to.")
    ] = "tokenizers",
):
    os.environ["TRANSFORMERS_CACHE"] = str(Path(directory).absolute() / "huggingface")

    from transformers import GPT2TokenizerFast

    GPT2TokenizerFast.from_pretrained("gpt2")

    os.environ["TIKTOKEN_CACHE_DIR"] = str(Path(directory).absolute() / "tiktoken")

    list(map(tiktoken.get_encoding, set(tiktoken.model.MODEL_TO_ENCODING.values())))

    print(f"Tokenizers downloaded to [green]{Path(directory).absolute()}[/green]")
    print(
        "Set the TIKTOKEN_CACHE_DIR environment variable to [green]"
        f"{Path(directory).absolute() / 'tiktoken'}[/green]"
    )
    print(
        f"Set the TRANSFORMERS_CACHE environment variable to [green]"
        f"{Path(directory).absolute() / 'huggingface'}[/green]"
    )
