import click
import typer
from rich import print
from typing_extensions import Annotated

from janus.llm.models_info import MODEL_TYPE_CONSTRUCTORS

llm = typer.Typer(
    help="LLM commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@llm.command("add", help="Add a model config to janus")
def llm_add(
    model_name: Annotated[
        str, typer.Argument(help="The user's custom name of the model")
    ],
    model_type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The type of the model",
            click_type=click.Choice(sorted(list(MODEL_TYPE_CONSTRUCTORS.keys()))),
        ),
    ] = "Azure",
):
    import json

    from janus.llm.models_info import (
        COST_PER_1K_TOKENS,
        MODEL_CONFIG_DIR,
        MODEL_ID_TO_LONG_ID,
        TOKEN_LIMITS,
        azure_models,
        bedrock_models,
        openai_models,
    )

    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_cfg = MODEL_CONFIG_DIR / f"{model_name}.json"
    if model_type == "HuggingFace":
        url = typer.prompt("Enter the model's URL")
        max_tokens = typer.prompt(
            "Enter the model's token limit", default=65536, type=int
        )
        max_tokens = typer.prompt(
            "Enter the model's max output tokens", default=8192, type=int
        )
        in_cost = typer.prompt("Enter the cost per input token", default=0, type=float)
        out_cost = typer.prompt("Enter the cost per output token", default=0, type=float)
        params = dict(
            inference_server_url=url,
            max_new_tokens=max_tokens,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            timeout=240,
        )
        cfg = {
            "model_type": model_type,
            "model_id": "gpt-4o",  # This is a placeholder to use the Azure PromptEngine
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
            "input_token_proportion": 0.4,
        }
    elif model_type == "HuggingFaceLocal":
        model_id = typer.prompt("Enter the model ID")
        task = typer.prompt("Enter the task")
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=4096, type=int
        )
        in_cost = 0
        out_cost = 0
        params = {"model_id": model_id, "task": task}
        cfg = {
            "model_type": model_type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
            "input_token_proportion": 0.4,
        }
    elif model_type == "OpenAI":
        print("DEPRECATED: Use 'Azure' instead. CTRL+C to exit.")
        model_id = typer.prompt(
            "Enter the model ID (list model IDs with `janus llm ls -a`)",
            default="gpt-4o",
            type=click.Choice(openai_models),
            show_choices=False,
        )
        params = dict(
            model_name=model_name,
            temperature=0.7,
            n=1,
        )
        max_tokens = TOKEN_LIMITS[model_name]
        model_cost = COST_PER_1K_TOKENS[model_name]
        cfg = {
            "model_type": model_type,
            "model_id": model_id,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
            "input_token_proportion": 0.4,
        }
    elif model_type == "Azure":
        model_id = typer.prompt(
            "Enter the model ID (list model IDs with `janus llm ls -a`)",
            default="gpt-4o",
            type=click.Choice(azure_models),
            show_choices=False,
        )
        params = dict(
            # Azure uses the "azure_deployment" key for what we're calling "long_model_id"
            azure_deployment=MODEL_ID_TO_LONG_ID[model_id],
            temperature=0.7,
            n=1,
        )
        max_tokens = TOKEN_LIMITS[MODEL_ID_TO_LONG_ID[model_id]]
        model_cost = COST_PER_1K_TOKENS[MODEL_ID_TO_LONG_ID[model_id]]
        cfg = {
            "model_type": model_type,
            "model_id": model_id,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
            "input_token_proportion": 0.4,
        }
    elif model_type == "BedrockChat" or model_type == "Bedrock":
        model_id = typer.prompt(
            "Enter the model ID (list model IDs with `janus llm ls -a`)",
            default="bedrock-claude-sonnet",
            type=click.Choice(bedrock_models),
            show_choices=False,
        )
        params = dict(
            # Bedrock uses the "model_id" key for what we're calling "long_model_id"
            model_id=MODEL_ID_TO_LONG_ID[model_id],
            model_kwargs={"temperature": 0.7},
        )
        max_tokens = TOKEN_LIMITS[MODEL_ID_TO_LONG_ID[model_id]]
        model_cost = COST_PER_1K_TOKENS[MODEL_ID_TO_LONG_ID[model_id]]
        cfg = {
            "model_type": model_type,
            "model_id": model_id,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
            "input_token_proportion": 0.4,
        }
    else:
        raise ValueError(f"Unknown model type {model_type}")
    with open(model_cfg, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Model config written to {model_cfg}")


@llm.command("ls", help="List all of the user-configured models")
def llm_ls(
    all: Annotated[
        bool,
        typer.Option(
            "--all",
            "-a",
            is_flag=True,
            help="List all models, including the default model IDs.",
            click_type=click.Choice(sorted(list(MODEL_TYPE_CONSTRUCTORS.keys()))),
        ),
    ] = False,
):
    import json

    from janus.llm.models_info import MODEL_CONFIG_DIR, MODEL_TYPES

    print("\n[green]User-configured models[/green]:")
    for model_cfg in MODEL_CONFIG_DIR.glob("*.json"):
        with open(model_cfg, "r") as f:
            cfg = json.load(f)
        print(f"\t[blue]{model_cfg.stem}[/blue]: [purple]{cfg['model_type']}[/purple]")

    if all:
        print("\n[green]Available model IDs[/green]:")
        for model_id, model_type in MODEL_TYPES.items():
            print(f"\t[blue]{model_id}[/blue]: [purple]{model_type}[/purple]")
