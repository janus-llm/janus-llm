import json
import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_community.llms.bedrock import Bedrock
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

from janus.prompts.prompt import (
    ChatGptPromptEngine,
    ClaudePromptEngine,
    Llama2PromptEngine,
    PromptEngine,
)

load_dotenv()

MODEL_TYPE_CONSTRUCTORS: dict[str, Callable[[Any], BaseLanguageModel]] = {
    "OpenAI": ChatOpenAI,
    "HuggingFace": HuggingFaceTextGenInference,
    "HuggingFaceLocal": HuggingFacePipeline.from_model_id,
    "Bedrock": Bedrock,
}

MODEL_PROMPT_ENGINES: dict[str, type[PromptEngine]] = {
    "gpt-4": ChatGptPromptEngine,
    "gpt-4-0613": ChatGptPromptEngine,
    "gpt-4-32k": ChatGptPromptEngine,
    "gpt-4-1106-preview": ChatGptPromptEngine,
    "gpt-4-0125-preview": ChatGptPromptEngine,
    "gpt-3.5-turbo": ChatGptPromptEngine,
    "gpt-3.5-turbo-0125": ChatGptPromptEngine,
    "bedrock-claude-haiku": ClaudePromptEngine,
    "meta.llama2-70b-v1": Llama2PromptEngine,
}


MODEL_TYPES: dict[str, str] = {
    "gpt-4": "OpenAI",
    "gpt-4-0613": "OpenAI",
    "gpt-4-32k": "OpenAI",
    "gpt-4-1106-preview": "OpenAI",
    "gpt-4-0125-preview": "OpenAI",
    "gpt-3.5-turbo": "OpenAI",
    "gpt-3.5-turbo-0125": "OpenAI",
    "bedrock-claude-haiku": "Bedrock",
    "meta.llama2-70b-v1": "Bedrock",
}

_open_ai_defaults: dict[str, str] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "openai_organization": os.getenv("OPENAI_ORG_ID"),
}

MODEL_DEFAULT_ARGUMENTS: dict[str, dict[str, str]] = {
    "gpt-4": dict(model_name="gpt-4"),
    "gpt-4-0613": dict(model_name="gpt-4-0613"),
    "gpt-4-32k": dict(model_name="gpt-4-32k"),
    "gpt-4-1106-preview": dict(model_name="gpt-4-1106-preview"),
    "gpt-4-0125-preview": dict(model_name="gpt-4-0125-preview"),
    "gpt-3.5-turbo": dict(model_name="gpt-3.5-turbo"),
    "gpt-3.5-turbo-0125": dict(model_name="gpt-3.5-turbo-0125"),
    "bedrock-claude-haiku": dict(model_name="anthropic.claude-3-haiku-20240307-v1:0"),
    "meta.llama2-70b-v1": dict(model_name="meta.llama2-70b-v1"),
}

DEFAULT_MODELS = list(MODEL_DEFAULT_ARGUMENTS.keys())

MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "llm"

TOKEN_LIMITS: dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32_768,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0125": 16_384,
    "text-embedding-ada-002": 8191,
    "gpt4all": 16_384,
    "bedrock-claude-haiku": 248_000,
    "meta.llama2-70b-v1": 4096,
}

COST_PER_MODEL: dict[str, dict[str, float]] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-0613": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-0125": {"input": 0.003, "output": 0.004},
    "bedrock-claude-haiku": {"input": 0.0, "output": 0.0},
    "meta.llama2-70b-v1": {"input": 0.0, "output": 0.0},
}


def load_model(model_name: str) -> tuple[BaseLanguageModel, int, dict[str, float]]:
    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_config_file = MODEL_CONFIG_DIR / f"{model_name}.json"
    if not model_config_file.exists():
        if model_name not in DEFAULT_MODELS:
            raise ValueError(f"Error: could not find model {model_name}")
        model_config = {
            "model_type": MODEL_TYPES[model_name],
            "model_args": MODEL_DEFAULT_ARGUMENTS[model_name],
            "token_limit": TOKEN_LIMITS.get(model_name, 4096),
            "model_cost": COST_PER_MODEL.get(model_name, {"input": 0, "output": 0}),
        }
        with open(model_config_file, "w") as f:
            json.dump(model_config, f)
    else:
        with open(model_config_file, "r") as f:
            model_config = json.load(f)
    model_constructor = MODEL_TYPE_CONSTRUCTORS[model_config["model_type"]]
    model_args = model_config["model_args"]
    if model_config["model_type"] == "OpenAI":
        model_args.update(_open_ai_defaults)
    model = model_constructor(**model_args)
    return model, model_config["token_limit"], model_config["model_cost"]
