import json
import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from langchain_community.chat_models import BedrockChat
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_community.llms.bedrock import Bedrock
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

from janus.llm.model_callbacks import COST_PER_1K_TOKENS
from janus.prompts.prompt import (
    ChatGptPromptEngine,
    ClaudePromptEngine,
    CoherePromptEngine,
    Llama2PromptEngine,
    Llama3PromptEngine,
    PromptEngine,
    TitanPromptEngine,
)

load_dotenv()

openai_model_reroutes = {
    "gpt-4o": "gpt-4o-2024-05-13",
    "gpt-4": "gpt-4-0613",
    "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo-preview": "gpt-4-0125-preview",
    "gpt-3.5-turbo": "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-0125",
}

openai_models = [
    "gpt-4-0613",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4o-2024-05-13",
    "gpt-3.5-turbo-0125",
]
claude_models = [
    "bedrock-claude-v2",
    "bedrock-claude-instant-v1",
    "bedrock-claude-haiku",
    "bedrock-claude-sonnet",
]
llama2_models = [
    "bedrock-llama2-70b",
    "bedrock-llama2-70b-chat",
    "bedrock-llama2-13b",
    "bedrock-llama2-13b-chat",
]
llama3_models = [
    "bedrock-llama3-8b-instruct",
    "bedrock-llama3-70b-instruct",
]
titan_models = [
    "bedrock-titan-text-lite",
    "bedrock-titan-text-express",
    "bedrock-jurassic-2-mid",
    "bedrock-jurassic-2-ultra",
]
cohere_models = [
    "bedrock-command-r-plus",
]
bedrock_models = [
    *claude_models,
    *llama2_models,
    *llama3_models,
    *titan_models,
    *cohere_models,
]
all_models = [*openai_models, *bedrock_models]

MODEL_TYPE_CONSTRUCTORS: dict[str, Callable[[Any], BaseLanguageModel]] = {
    "OpenAI": ChatOpenAI,
    "HuggingFace": HuggingFaceTextGenInference,
    "HuggingFaceLocal": HuggingFacePipeline.from_model_id,
    "Bedrock": Bedrock,
    "BedrockChat": BedrockChat,
}


MODEL_PROMPT_ENGINES: dict[str, Callable[..., PromptEngine]] = {
    **{m: ChatGptPromptEngine for m in openai_models},
    **{m: ClaudePromptEngine for m in claude_models},
    **{m: Llama2PromptEngine for m in llama2_models},
    **{m: Llama3PromptEngine for m in llama3_models},
    **{m: TitanPromptEngine for m in titan_models},
    **{m: CoherePromptEngine for m in cohere_models},
}

_open_ai_defaults: dict[str, str] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "openai_organization": os.getenv("OPENAI_ORG_ID"),
}

model_identifiers = {
    **{m: m for m in openai_models},
    "bedrock-claude-v2": "anthropic.claude-v2",
    "bedrock-claude-instant-v1": "anthropic.claude-instant-v1",
    "bedrock-claude-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "bedrock-claude-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "bedrock-llama2-70b": "meta.llama2-70b-v1",
    "bedrock-llama2-70b-chat": "meta.llama2-70b-chat-v1",
    "bedrock-llama2-13b": "meta.llama2-13b-chat-v1",
    "bedrock-llama2-13b-chat": "meta.llama2-13b-v1",
    "bedrock-llama3-8b-instruct": "meta.llama3-8b-instruct-v1:0",
    "bedrock-llama3-70b-instruct": "meta.llama3-70b-instruct-v1:0",
    "bedrock-titan-text-lite": "amazon.titan-text-lite-v1",
    "bedrock-titan-text-express": "amazon.titan-text-express-v1",
    "bedrock-jurassic-2-mid": "ai21.j2-mid-v1",
    "bedrock-jurassic-2-ultra": "ai21.j2-ultra-v1",
    "bedrock-command-r-plus": "cohere.command-r-plus-v1:0",
}

MODEL_DEFAULT_ARGUMENTS: dict[str, dict[str, str]] = {
    k: (dict(model_name=k) if k in openai_models else dict(model_id=v))
    for k, v in model_identifiers.items()
}

DEFAULT_MODELS = list(MODEL_DEFAULT_ARGUMENTS.keys())

MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "llm"

MODEL_TYPES: dict[str, PromptEngine] = {
    **{model_identifiers[m]: "OpenAI" for m in openai_models},
    **{model_identifiers[m]: "BedrockChat" for m in bedrock_models},
}

TOKEN_LIMITS: dict[str, int] = {
    "gpt-4-32k": 32_768,
    "gpt-4-0613": 8192,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-4o-2024-05-13": 128_000,
    "gpt-3.5-turbo-0125": 16_384,
    "text-embedding-ada-002": 8191,
    "gpt4all": 16_384,
    "anthropic.claude-v2": 100_000,
    "anthropic.claude-instant-v1": 100_000,
    "anthropic.claude-3-haiku-20240307-v1:0": 248_000,
    "anthropic.claude-3-sonnet-20240229-v1:0": 248_000,
    "meta.llama2-70b-v1": 4096,
    "meta.llama2-70b-chat-v1": 4096,
    "meta.llama2-13b-chat-v1": 4096,
    "meta.llama2-13b-v1": 4096,
    "meta.llama3-8b-instruct-v1:0": 8000,
    "meta.llama3-70b-instruct-v1:0": 8000,
    "amazon.titan-text-lite-v1": 4096,
    "amazon.titan-text-express-v1": 8192,
    "ai21.j2-mid-v1": 8192,
    "ai21.j2-ultra-v1": 8192,
    "cohere.command-r-plus-v1:0": 128_000,
}


def load_model(model_name: str) -> tuple[BaseLanguageModel, int, dict[str, float]]:
    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_config_file = MODEL_CONFIG_DIR / f"{model_name}.json"
    if not model_config_file.exists():
        if model_name not in DEFAULT_MODELS:
            if model_name in openai_model_reroutes:
                model_name = openai_model_reroutes[model_name]
            else:
                raise ValueError(f"Error: could not find model {model_name}")
        model_config = {
            "model_type": MODEL_TYPES[model_name],
            "model_args": MODEL_DEFAULT_ARGUMENTS[model_name],
            "token_limit": TOKEN_LIMITS.get(model_identifiers[model_name], 4096),
            "model_cost": COST_PER_1K_TOKENS.get(
                model_identifiers[model_name], {"input": 0, "output": 0}
            ),
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
