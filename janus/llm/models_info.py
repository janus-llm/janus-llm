import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL_TYPE_CONSTRUCTORS: dict[str, Callable[[Any], BaseLanguageModel]] = {
    "OpenAI": ChatOpenAI,
    "HuggingFace": HuggingFaceTextGenInference,
    "HuggingFaceLocal": HuggingFacePipeline.from_model_id,
}


MODEL_TYPES: Dict[str, Any] = {
    "gpt-4": "OpenAI",
    "gpt-4-32k": "OpenAI",
    "gpt-4-1106-preview": "OpenAI",
    "gpt-4-0125-preview": "OpenAI",
    "gpt-3.5-turbo": "OpenAI",
    "gpt-3.5-turbo-16k": "OpenAI",
}

_open_ai_defaults: Dict[str, Any] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "openai_organization": os.getenv("OPENAI_ORG_ID"),
}

MODEL_DEFAULT_ARGUMENTS: Dict[str, Dict[str, Any]] = {
    "gpt-4": dict(model_name="gpt-4"),
    "gpt-4-32k": dict(model_name="gpt-4-32k"),
    "gpt-4-1106-preview": dict(model_name="gpt-4-1106-preview"),
    "gpt-4-0125-preview": dict(model_name="gpt-4-0125-preview"),
    "gpt-3.5-turbo": dict(model_name="gpt-3.5-turbo"),
    "gpt-3.5-turbo-16k": dict(model_name="gpt-3.5-turbo-16k"),
}

DEFAULT_MODELS = list(MODEL_DEFAULT_ARGUMENTS.keys())

MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "llm"

TOKEN_LIMITS: Dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32_768,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16_384,
    "text-embedding-ada-002": 8191,
    "gpt4all": 16_384,
}

COST_PER_MODEL: Dict[str, Dict[str, float]] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
}


def load_model(model_name: str) -> Tuple[BaseLanguageModel, int, Dict[str, float]]:
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
