import os
from typing import Any, Dict

from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceTextGenInference

MODEL_CONSTRUCTORS: Dict[str, Any] = {
    "gpt-4": ChatOpenAI,
    "gpt-4-32k": ChatOpenAI,
    "gpt-3.5-turbo": ChatOpenAI,
    "gpt-3.5-turbo-16k": ChatOpenAI,
    "llama": HuggingFaceTextGenInference,
    "falcon": HuggingFaceTextGenInference,
}

_open_ai_defaults: Dict[str, Any] = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    # "openai_organization": os.getenv("OPENAI_ORG_ID")
}

MODEL_DEFAULT_ARGUMENTS: Dict[str, Dict[str, Any]] = {
    "gpt-4": dict(model_name="gpt-4", **_open_ai_defaults),
    "gpt-4-32k": dict(model_name="gpt-4-32k", **_open_ai_defaults),
    "gpt-3.5-turbo": dict(model_name="gpt-3.5-turbo", **_open_ai_defaults),
    "gpt-3.5-turbo-16k": dict(model_name="gpt-3.5-turbo-16k", **_open_ai_defaults),
    "llama": dict(
        inference_server_url="https://llama-aip.lt.mitre.org",
        max_new_tokens=512,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        repetition_penalty=1.03,
    ),
    "falcon": dict(
        inference_server_url="https://falcon-aip.lt.mitre.org/",
        max_new_tokens=512,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        repetition_penalty=1.03,
    ),
}

TOKEN_LIMITS: Dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "falcon": 1024,
}

COST_PER_MODEL: Dict[str, Dict[str, float]] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    "llama": {"input": 0.0, "output": 0.0},
    "falcon": {"input": 0.0, "output": 0.0},
}
