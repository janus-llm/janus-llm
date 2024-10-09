import threading
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, LLMResult
from langchain_core.tracers.context import register_configure_hook

from janus.utils.logger import create_logger

log = create_logger(__name__)

openai_model_reroutes = {
    "gpt-4o": "gpt-4o-2024-05-13",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4": "gpt-4-0613",
    "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo-preview": "gpt-4-0125-preview",
    "gpt-3.5-turbo": "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k-0613": "gpt-3.5-turbo-0125",
}


# Updated 2024-06-21
COST_PER_1K_TOKENS: dict[str, dict[str, float]] = {
    "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
    "gpt-4-0613": {"input": 0.03, "output": 0.06},
    "gpt-4o-2024-05-13": {"input": 0.005, "output": 0.015},
    "anthropic.claude-v2": {"input": 0.008, "output": 0.024},
    "anthropic.claude-instant-v1": {"input": 0.0008, "output": 0.0024},
    "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.00025, "output": 0.00125},
    "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.003, "output": 0.015},
    "meta.llama2-13b-chat-v1": {"input": 0.00075, "output": 0.001},
    "meta.llama2-70b-chat-v1": {"input": 0.00195, "output": 0.00256},
    "meta.llama2-13b-v1": {"input": 0.0, "output": 0.0},
    "meta.llama2-70b-v1": {"input": 0.00265, "output": 0.0035},
    "meta.llama3-8b-instruct-v1:0": {"input": 0.0003, "output": 0.0006},
    "meta.llama3-70b-instruct-v1:0": {"input": 0.00265, "output": 0.0035},
    "amazon.titan-text-lite-v1": {"input": 0.00015, "output": 0.0002},
    "amazon.titan-text-express-v1": {"input": 0.0002, "output": 0.0006},
    "ai21.j2-mid-v1": {"input": 0.0125, "output": 0.0125},
    "ai21.j2-ultra-v1": {"input": 0.0188, "output": 0.0188},
    "cohere.command-r-plus-v1:0": {"input": 0.003, "output": 0.015},
    "mistral.mistral-7b-instruct-v0:2": {"input": 0.00015, "output": 0.0002},
    "mistral.mixtral-8x7b-instruct-v0:1": {"input": 0.00045, "output": 0.0007},
    "mistral.mistral-large-2402-v1:0": {"input": 0.004, "output": 0.012},
}


def _get_token_cost(
    prompt_tokens: int, completion_tokens: int, model_id: str | None
) -> float:
    """Get the cost of tokens according to model ID"""
    if model_id in openai_model_reroutes:
        model_id = openai_model_reroutes[model_id]
    if model_id not in COST_PER_1K_TOKENS:
        raise ValueError(
            f"Unknown model: {model_id}. Please provide a valid model name."
            f" Known models are: {', '.join(COST_PER_1K_TOKENS.keys())}"
        )
    model_cost = COST_PER_1K_TOKENS[model_id]
    input_cost = (prompt_tokens / 1000.0) * model_cost["input"]
    output_cost = (completion_tokens / 1000.0) * model_cost["output"]
    return input_cost + output_cost


class TokenUsageCallbackHandler(BaseCallbackHandler):
    """Callback Handler that tracks metadata on model cost, retries, etc.
    Based on https://github.com/langchain-ai/langchain/blob/master/libs
                /community/langchain_community/callbacks/openai_info.py
    """

    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    successful_requests: int = 0
    total_cost: float = 0.0

    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()

    def __repr__(self) -> str:
        return (
            f"Tokens Used: {self.total_tokens}\n"
            f"\tPrompt Tokens: {self.prompt_tokens}\n"
            f"\tCompletion Tokens: {self.completion_tokens}\n"
            f"Successful Requests: {self.successful_requests}\n"
            f"Total Cost (USD): ${self.total_cost}"
        )

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_chat_model_start(self, *args, **kwargs):
        pass

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Print out the token."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Collect token usage."""
        # Check for usage_metadata (langchain-core >= 0.2.2)
        try:
            generation = response.generations[0][0]
        except IndexError:
            generation = None

        model_id = ""
        usage_metadata = None
        if hasattr(response, "llm_output") and response.llm_output is not None:
            model_id = response.llm_output.get("model_id", model_id)
            model_id = response.llm_output.get("model_name", model_id)
            usage_metadata = response.llm_output.get("usage", usage_metadata)
            usage_metadata = response.llm_output.get("token_usage", usage_metadata)
        elif isinstance(generation, ChatGeneration):
            if hasattr(generation, "response_metadata"):
                model_id = generation.response_metadata.get("model_id", model_id)
                model_id = generation.response_metadata.get("model_name", model_id)
                usage_metadata = generation.response_metadata.get("usage", usage_metadata)
            elif hasattr(generation, "message"):
                if isinstance(generation.message, AIMessage):
                    usage_metadata = generation.message.usage_metadata

        completion_tokens = 0
        prompt_tokens = 0
        total_tokens = 0
        if usage_metadata:
            prompt_tokens = usage_metadata.get("prompt_tokens", prompt_tokens)
            prompt_tokens = usage_metadata.get("input_tokens", prompt_tokens)
            completion_tokens = usage_metadata.get("completion_tokens", completion_tokens)
            completion_tokens = usage_metadata.get("output_tokens", completion_tokens)
            total_tokens = usage_metadata.get("total_tokens", total_tokens)
        else:
            with self._lock:
                self.successful_requests += 1
            return None

        total_cost = _get_token_cost(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_id=model_id,
        )

        # update shared state behind lock
        with self._lock:
            self.total_cost += total_cost
            self.total_tokens += total_tokens
            self.prompt_tokens += prompt_tokens
            self.completion_tokens += completion_tokens
            self.successful_requests += 1

    def __copy__(self) -> "TokenUsageCallbackHandler":
        """Return a copy of the callback handler."""
        return self

    def __deepcopy__(self, memo: Any) -> "TokenUsageCallbackHandler":
        """Return a deep copy of the callback handler."""
        return self


token_usage_callback_var: ContextVar[TokenUsageCallbackHandler | None] = ContextVar(
    "token_usage_callback_var", default=None
)
register_configure_hook(token_usage_callback_var, True)


@contextmanager
def get_model_callback() -> Generator[TokenUsageCallbackHandler, None, None]:
    cb = TokenUsageCallbackHandler()
    token_usage_callback_var.set(cb)
    yield cb
    token_usage_callback_var.set(None)
