import click
import typer
from typing_extensions import Annotated

from janus.embedding.embedding_models_info import EmbeddingModelType

embedding = typer.Typer(
    help="Embedding model commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@embedding.command("add", help="Add an embedding model config to janus")
def embedding_add(
    model_name: Annotated[
        str, typer.Argument(help="The user's custom name for the model")
    ],
    model_type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The type of the model",
            click_type=click.Choice(list(val.value for val in EmbeddingModelType)),
        ),
    ] = "OpenAI",
):
    import json
    from pathlib import Path

    from pydantic import AnyHttpUrl

    from janus.embedding.embedding_models_info import (
        EMBEDDING_COST_PER_MODEL,
        EMBEDDING_MODEL_CONFIG_DIR,
        EMBEDDING_TOKEN_LIMITS,
    )

    if not EMBEDDING_MODEL_CONFIG_DIR.exists():
        EMBEDDING_MODEL_CONFIG_DIR.mkdir(parents=True)
    model_cfg = EMBEDDING_MODEL_CONFIG_DIR / f"{model_name}.json"
    if model_type in EmbeddingModelType.HuggingFaceInferenceAPI.values:
        hf = typer.style("HuggingFaceInferenceAPI", fg="yellow")
        url = typer.prompt(f"Enter the {hf} model's URL", type=str, value_proc=AnyHttpUrl)
        api_model_name = typer.prompt("Enter the model's name", type=str, default="")
        api_key = typer.prompt("Enter the API key", type=str, default="")
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=8191, type=int
        )
        in_cost = typer.prompt("Enter the cost per input token", default=0, type=float)
        out_cost = typer.prompt("Enter the cost per output token", default=0, type=float)
        params = dict(
            model_name=api_model_name,
            api_key=api_key,
        )
        cfg = {
            "model_type": model_type,
            "model_identifier": str(url),
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
        }
    elif model_type in EmbeddingModelType.HuggingFaceLocal.values:
        hf = typer.style("HuggingFace", fg="yellow")
        model_id = typer.prompt(
            f"Enter the {hf} model ID",
            default="sentence-transformers/all-MiniLM-L6-v2",
            type=str,
        )
        cache_folder = str(
            Path(
                typer.prompt(
                    "Enter the model's cache folder",
                    default=EMBEDDING_MODEL_CONFIG_DIR / "cache",
                    type=str,
                )
            )
        )
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=8191, type=int
        )
        params = dict(
            cache_folder=str(cache_folder),
        )
        cfg = {
            "model_type": model_type,
            "model_identifier": model_id,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": 0, "output": 0},
        }
    elif model_type in EmbeddingModelType.OpenAI.values:
        available_models = list(EMBEDDING_COST_PER_MODEL.keys())

        open_ai = typer.style("OpenAI", fg="green")
        prompt = f"Enter the {open_ai} model name"

        model_name = typer.prompt(
            prompt,
            default="text-embedding-3-small",
            type=click.types.Choice(available_models),
            show_choices=False,
        )
        params = dict(
            model=model_name,
        )
        max_tokens = EMBEDDING_TOKEN_LIMITS[model_name]
        model_cost = EMBEDDING_COST_PER_MODEL[model_name]
        cfg = {
            "model_type": model_type,
            "model_identifier": model_name,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
        }
    else:
        raise ValueError(f"Unknown model type {model_type}")
    with open(model_cfg, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Model config written to {model_cfg}")
