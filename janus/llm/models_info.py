import json
import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_community.llms.bedrock import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel

from janus.prompts.prompt import (
    ChatGptPromptEngine,
    ClaudePromptEngine,
    Llama2PromptEngine,
    Llama3PromptEngine,
    TitanPromptEngine,
    CoherePromptEngine,
    PromptEngine,
)

load_dotenv()

MODEL_TYPE_CONSTRUCTORS: dict[str, Callable[[Any], BaseLanguageModel]] = {
    "OpenAI": ChatOpenAI,
    "HuggingFace": HuggingFaceTextGenInference,
    "HuggingFaceLocal": HuggingFacePipeline.from_model_id,
    "Bedrock": Bedrock,
    "BedrockChat": BedrockChat,
}

MODEL_PROMPT_ENGINES: dict[str, type[PromptEngine]] = {
    "gpt-4": ChatGptPromptEngine,
    "gpt-4-32k": ChatGptPromptEngine,
    "gpt-4-1106-preview": ChatGptPromptEngine,
    "gpt-4-0125-preview": ChatGptPromptEngine,
    "gpt-3.5-turbo": ChatGptPromptEngine,
    "gpt-3.5-turbo-16k": ChatGptPromptEngine,
    "bedrock-claude-v2": ClaudePromptEngine,
    "bedrock-claude-instant-v1": ClaudePromptEngine,
    "bedrock-claude-haiku": ClaudePromptEngine,
    "bedrock-claude-sonnet": ClaudePromptEngine,
    "bedrock-llama2-70b": Llama2PromptEngine,
    "bedrock-llama2-70b-chat": Llama2PromptEngine,
    "bedrock-llama2-13b": Llama2PromptEngine,
    "bedrock-llama2-13b-chat": Llama2PromptEngine,
    "bedrock-llama3-8b-instruct": Llama3PromptEngine,
    "bedrock-llama3-70b-instruct": Llama3PromptEngine,
    "bedrock-titan-text-lite": TitanPromptEngine,
    "bedrock-titan-text-express": TitanPromptEngine,
    "bedrock-jurassic-2-mid": TitanPromptEngine,
    "bedrock-jurassic-2-ultra": TitanPromptEngine,
    "bedrock-command-r-plus": CoherePromptEngine,
}


MODEL_TYPES: dict[str, str] = {
    "gpt-4": "OpenAI",
    "gpt-4-32k": "OpenAI",
    "gpt-4-1106-preview": "OpenAI",
    "gpt-4-0125-preview": "OpenAI",
    "gpt-3.5-turbo": "OpenAI",
    "gpt-3.5-turbo-16k": "OpenAI",
    "anthropic.claude-v2": "BedrockChat",
    "anthropic.claude-instant-v1": "BedrockChat",
    "anthropic.claude-3-haiku-20240307-v1:0": "BedrockChat",
    "anthropic.claude-3-sonnet-20240229-v1:0": "BedrockChat",
    "meta.llama2-70b-v1": "BedrockChat",
    "meta.llama2-70b-chat-v1": "BedrockChat",
    "meta.llama2-13b-chat-v1": "BedrockChat",
    "meta.llama2-13b-v1": "BedrockChat",
    "meta.llama3-8b-instruct-v1:0": "BedrockChat",
    "meta.llama3-70b-instruct-v1:0": "BedrockChat",
    "amazon.titan-text-lite-v1": "BedrockChat",
    "amazon.titan-text-express-v1": "BedrockChat",
    "ai21.j2-mid-v1": "Bedrock",
    "ai21.j2-ultra-v1": "Bedrock",
    "cohere.command-r-plus-v1:0": "BedrockChat",
}

_open_ai_defaults: dict[str, str] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "openai_organization": os.getenv("OPENAI_ORG_ID"),
}

MODEL_DEFAULT_ARGUMENTS: dict[str, dict[str, str]] = {
    "gpt-4": dict(model_name="gpt-4"),
    "gpt-4-32k": dict(model_name="gpt-4-32k"),
    "gpt-4-1106-preview": dict(model_name="gpt-4-1106-preview"),
    "gpt-4-0125-preview": dict(model_name="gpt-4-0125-preview"),
    "gpt-3.5-turbo": dict(model_name="gpt-3.5-turbo"),
    "gpt-3.5-turbo-16k": dict(model_name="gpt-3.5-turbo-16k"),
    "anthropic.claude-v2": dict(model_name="anthropic.claude-v2"),
    "anthropic.claude-instant-v1": dict(model_name="anthropic.claude-instant-v1"),
    "anthropic.claude-3-haiku-20240307-v1:0": dict(
        model_name="anthropic.claude-3-haiku-20240307-v1:0"
    ),
    "anthropic.claude-3-sonnet-20240229-v1:0": dict(
        model_name="anthropic.claude-3-sonnet-20240229-v1:0"
    ),
    "meta.llama2-70b-v1": dict(model_name="meta.llama2-70b-v1"),
    "meta.llama2-70b-chat-v1": dict(model_name="meta.llama2-70b-chat-v1"),
    "meta.llama2-13b-chat-v1": dict(model_name="meta.llama2-13b-chat-v1"),
    "meta.llama2-13b-v1": dict(model_name="meta.llama2-13b-v1"),
    "meta.llama3-8b-instruct-v1:0": dict(model_name="meta.llama3-8b-instruct-v1:0"),
    "meta.llama3-70b-instruct-v1:0": dict(model_name="meta.llama3-70b-instruct-v1:0"),
    "amazon.titan-text-lite-v1": dict(model_name="amazon.titan-text-lite-v1"),
    "amazon.titan-text-express-v1": dict(model_name="amazon.titan-text-express-v1"),
    "ai21.j2-mid-v1": dict(model_name="ai21.j2-mid-v1"),
    "ai21.j2-ultra-v1": dict(model_name="ai21.j2-ultra-v1"),
    "cohere.command-r-plus-v1:0": dict(model_name="cohere.command-r-plus-v1:0"),
}

DEFAULT_MODELS = list(MODEL_DEFAULT_ARGUMENTS.keys())

MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "llm"

TOKEN_LIMITS: dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32_768,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16_384,
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
    "cohere.command-r-plus-v1:0":  128_000
}

COST_PER_MODEL: dict[str, dict[str, float]] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    "anthropic.claude-v2": {"input": 0.0, "output": 0.0},
    "anthropic.claude-instant-v1": {"input": 0.0, "output": 0.0},
    "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.00025, "output": 0.00125},
    "anthropic.claude-3-sonnet-20240307-v1:0": {"input": 0.003, "output": 0.015},
    "meta.llama2-70b-v1": {"input": 0.00265, "output": 0.0035},
    "meta.llama2-70b-chat-v1": {"input": 0.00195, "output": 0.00256},
    "meta.llama2-13b-chat-v1": {"input": 0.00075, "output": 0.001},
    "meta.llama2-13b-v1": {"input": 0.0, "output": 0.0},
    "meta.llama3-8b-instruct-v1:0": {"input": 0.0004, "output": 0.0006},
    "meta.llama3-70b-instruct-v1:0": {"input": 0.00265, "output": 0.0035},
    "amazon.titan-text-lite-v1": {"input": 0.0, "output": 0.0},
    "amazon.titan-text-express-v1": {"input": 0.0, "output": 0.0},
    "ai21.j2-mid-v1": {"input": 0.0125, "output": 0.0125},
    "ai21.j2-ultra-v1": {"input": 0.0188, "output": 0.0188},
    "cohere.command-r-plus-v1:0": {"input": 0.003, "output": 0.015},
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
