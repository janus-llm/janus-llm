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
    "text-embedding-3-small": "OpenAI",
    "text-embedding-3-large": "OpenAI",
    "text-embedding-ada-002": "OpenAI",
}

_open_ai_defaults: Dict[str, Any] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "openai_organization": os.getenv("OPENAI_ORG_ID"),
}

EMBEDDING_MODEL_DEFAULT_ARGUMENTS: Dict[str, Dict[str, Any]] = {
    "text-embedding-3-small": dict(model="text-embedding-3-small"),
    "text-embedding-3-large": dict(model="text-embedding-3-large"),
    "text-embedding-ada-002": dict(model="text-embedding-ada-002"),
}

DEFAULT_EMBEDDING_MODELS = list(EMBEDDING_MODEL_DEFAULT_ARGUMENTS.keys())

EMBEDDING_MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "embeddings"

EMBEDDING_TOKEN_LIMITS: Dict[str, int] = {
    "text-embedding-3-small": 8191,
    "text-embedding-3-large": 8191,
    "text-embedding-ada-002": 8191,
}

EMBEDDING_COST_PER_MODEL: Dict[str, float] = {
    "text-embedding-3-small": 1.0 / 62500,
    "text-embedding-3-large": 1.0 / 9615,
    "text-embedding-ada-002": 1.0 / 12500,
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
