import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_core.embeddings import Embeddings

load_dotenv()

EMBEDDING_MODEL_TYPE_CONSTRUCTORS: Dict[str, Callable[[Any], Embeddings]] = {
    "OpenAI": OpenAIEmbeddings,
    "HuggingFace": HuggingFaceEmbeddings,
}

EMBEDDING_MODEL_TYPES: Dict[str, Any] = {
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

EMBEDDING_MODEL_DEFAULT_ARGUMENTS: Dict[str, Dict[str, Any]] = {
    "gpt-4": dict(model="gpt-4"),
    "gpt-4-32k": dict(model="gpt-4-32k"),
    "gpt-4-1106-preview": dict(model="gpt-4-1106-preview"),
    "gpt-4-0125-preview": dict(model="gpt-4-0125-preview"),
    "gpt-3.5-turbo": dict(model="gpt-3.5-turbo"),
    "gpt-3.5-turbo-16k": dict(model="gpt-3.5-turbo-16k"),
}

DEFAULT_EMBEDDING_MODELS = list(EMBEDDING_MODEL_DEFAULT_ARGUMENTS.keys())

EMBEDDING_MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "embeddings"

EMBEDDING_TOKEN_LIMITS: Dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32_768,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16_384,
    "text-embedding-ada-002": 8191,
    "gpt4all": 16_384,
}

EMBEDDING_COST_PER_MODEL: Dict[str, Dict[str, float]] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
}


def load_embedding_model(model_name: str) -> Tuple[Embeddings, int, Dict[str, float]]:
    if not EMBEDDING_MODEL_CONFIG_DIR.exists():
        EMBEDDING_MODEL_CONFIG_DIR.mkdir(parents=True)
    model_config_file = EMBEDDING_MODEL_CONFIG_DIR / f"{model_name}.json"
    if not model_config_file.exists():
        if model_name not in DEFAULT_EMBEDDING_MODELS:
            raise ValueError(f"Error: could not find model {model_name}")
        model_config = {
            "model_type": EMBEDDING_MODEL_TYPES[model_name],
            "model_args": EMBEDDING_MODEL_DEFAULT_ARGUMENTS[model_name],
            "token_limit": EMBEDDING_TOKEN_LIMITS.get(model_name, 4096),
            "model_cost": EMBEDDING_COST_PER_MODEL.get(
                model_name, {"input": 0, "output": 0}
            ),
        }
        with open(model_config_file, "w") as f:
            json.dump(model_config, f)
    else:
        with open(model_config_file, "r") as f:
            model_config = json.load(f)
    model_constructor = EMBEDDING_MODEL_TYPE_CONSTRUCTORS[model_config["model_type"]]
    model_args = model_config["model_args"]
    if model_config["model_type"] == "OpenAI":
        model_args.update(_open_ai_defaults)
    model = model_constructor(**model_args)
    return model, model_config["token_limit"], model_config["model_cost"]
