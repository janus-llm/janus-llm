import json
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from aenum import MultiValueEnum
from dotenv import load_dotenv
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from janus.utils.logger import create_logger

load_dotenv()

log = create_logger(__name__)

try:
    from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
except ImportError:
    log.warning(
        "Could not import LangChain's HuggingFace Embeddings Client. If you would like "
        "to use HuggingFace models, please install LangChain's HuggingFace Embeddings "
        "Client by running 'pip install janus-embedding[hf-local]' or poetry install "
        "-E hf-local."
    )


class EmbeddingModelType(MultiValueEnum):
    OpenAI = "OpenAI", "openai", "open-ai", "oai"
    HuggingFaceLocal = "HuggingFaceLocal", "huggingfacelocal", "huggingface-local", "hfl"
    HuggingFaceInferenceAPI = (
        "HuggingFaceInferenceAPI",
        "huggingfaceinferenceapi",
        "huggingface-inference-api",
        "hfia",
    )


EMBEDDING_MODEL_TYPE_CONSTRUCTORS: Dict[
    EmbeddingModelType, Callable[[Any], Embeddings]
] = {}

for model_type in EmbeddingModelType:
    for value in model_type.values:
        if model_type == EmbeddingModelType.OpenAI:
            EMBEDDING_MODEL_TYPE_CONSTRUCTORS[value] = OpenAIEmbeddings
        elif model_type == EmbeddingModelType.HuggingFaceLocal:
            try:
                EMBEDDING_MODEL_TYPE_CONSTRUCTORS[value] = HuggingFaceEmbeddings
            except NameError:
                pass
        elif model_type == EmbeddingModelType.HuggingFaceInferenceAPI:
            EMBEDDING_MODEL_TYPE_CONSTRUCTORS[value] = HuggingFaceInferenceAPIEmbeddings

EMBEDDING_MODEL_TYPE_DEFAULT_IDS: Dict[EmbeddingModelType, Dict[str, Any]] = {
    EmbeddingModelType.OpenAI.value: "text-embedding-3-small",
    EmbeddingModelType.HuggingFaceLocal.value: "all-MiniLM-L6-v2",
    EmbeddingModelType.HuggingFaceInferenceAPI.value: "",
}

EMBEDDING_MODEL_DEFAULT_ARGUMENTS: Dict[str, Dict[str, Any]] = {
    "text-embedding-3-small": dict(model="text-embedding-3-small"),
    "text-embedding-3-large": dict(model="text-embedding-3-large"),
    "text-embedding-ada-002": dict(model="text-embedding-ada-002"),
}

EMBEDDING_MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "embeddings"

EMBEDDING_TOKEN_LIMITS: Dict[str, int] = {
    "text-embedding-3-small": 8191,
    "text-embedding-3-large": 8191,
    "text-embedding-ada-002": 8191,
}

EMBEDDING_COST_PER_MODEL: Dict[str, float] = {
    "text-embedding-3-small": {"input": 0.02 / 1e6, "output": 0.0},
    "text-embedding-3-large": {"input": 0.13 / 1e6, "output": 0.0},
    "text-embedding-ada-002": {"input": 0.10 / 1e6, "output": 0.0},
}


def load_embedding_model(
    model_name: str,
) -> Tuple[Embeddings, int, Dict[str, float]]:
    """Load an embedding model from the configuration file or create a new one

    Arguments:
        model_name: The user-given name of the model to load.
        model_type: The type of the model to load.
        identifier: The identifier for the model (e.g. the name, URL, or HuggingFace
            path).
    """
    if not EMBEDDING_MODEL_CONFIG_DIR.exists():
        EMBEDDING_MODEL_CONFIG_DIR.mkdir(parents=True)
    model_config_file = EMBEDDING_MODEL_CONFIG_DIR / f"{model_name}.json"

    if not model_config_file.exists():
        # The default model type is HuggingFaceLocal because that's the default for Chroma
        model_type = EmbeddingModelType.HuggingFaceLocal.value
        identifier = EMBEDDING_MODEL_TYPE_DEFAULT_IDS[model_type]
        model_config = {
            "model_type": model_type,
            "model_identifier": identifier,
            "model_args": EMBEDDING_MODEL_DEFAULT_ARGUMENTS.get(identifier, {}),
            "token_limit": EMBEDDING_TOKEN_LIMITS.get(identifier, 8191),
            "model_cost": EMBEDDING_COST_PER_MODEL.get(
                identifier, {"input": 0, "output": 0}
            ),
        }
        log.info(
            f"WARNING: Creating new model config file: \
                {model_config_file} with default config"
        )
        with open(model_config_file, "w") as f:
            json.dump(model_config, f, indent=2)
    else:
        with open(model_config_file, "r") as f:
            model_config = json.load(f)
    model_constructor = EMBEDDING_MODEL_TYPE_CONSTRUCTORS[model_config["model_type"]]
    model_args = model_config["model_args"]
    if model_config["model_type"] in EmbeddingModelType.HuggingFaceInferenceAPI.values:
        model_args.update({"api_url": model_config["model_identifier"]})
    elif model_config["model_type"] in EmbeddingModelType.HuggingFaceLocal.values:
        model_args.update({"model_name": model_config["model_identifier"]})
    model = model_constructor(**model_args)
    return (
        model,
        model_config["token_limit"],
        model_config["model_cost"],
    )
