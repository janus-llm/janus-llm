"""A module that defines..."""
from typing import Dict, Optional

from langchain.llms import OpenAI
from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from ..utils.logger import create_logger
from .custom import CustomLLM

log = create_logger(__name__)


MODEL_TYPES: Dict[str, str] = {
    "gpt-4": "chat-gpt",
    "gpt-4-32k": "chat-gpt",
    "gpt-3.5-turbo": "chat-gpt",
    "gpt-3.5-turbo-16k": "chat-gpt",
}

# From the OpenAI Docs:
# https://platform.openai.com/docs/models/gpt-4
# https://platform.openai.com/docs/models/gpt-3-5
TOKEN_LIMITS: Dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
}

# The cost per 1k tokens for each model at the input and output:
# https://openai.com/pricing
COST_PER_MODEL: Dict[str, float] = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.6, "output": 0.12},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
}


class MyOpenAI(CustomLLM):
    """A class to interact with the OpenAI LLMs."""

    def __init__(
        self,
        model: str,
        openai_api_key: str,
        openai_organization: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        num_completions: int = 1,
        batch_size: int = 20,
        max_retries: int = 6,
        request_timeout: float = 600,
    ) -> None:
        """Initialize the LLM.

        Arguments:
            model: The model to use for the LLM.
            openai_api_key: The OpenAI API key.
            openai_organization: The OpenAI organization.
            temperature: The temperature to use for the LLM.
            top_p: Total probability mass of tokens to consider at each step.
            max_tokens: The maximum number of tokens to generate in the completion.
                -1 returns as many tokens as possible given the prompt and
                the models maximal context size.
            presence_penalty: The presence penalty to use for the LLM. Penalizes repeated
                tokens.
            frequency_penalty: The frequency penalty to use for the LLM. Penalizes
                repeated tokens according to frequency.
            num_completions: The number of completions to generate for each prompt.
            batch_size: Batch size to use when passing multiple documents to generate.
            max_retries: The maximum number of retries to make when generating.
            request_timeout: Timeout for requests to OpenAI completion API. Default is
                600 seconds.

        See [here](https://platform.openai.com/docs/api-reference/chat/create) for more
        documentation on each variable.

        Raises:
            ValueError: If the model is not supported.
        """
        self.model = model
        if model not in list(MODEL_TYPES.keys()):
            raise ValueError(
                f"Model {model} not supported. Select from one of the "
                f"following: {list(MODEL_TYPES.keys())}"
            )
        self._langchain_model = OpenAI(
            model=model,
            openai_api_key=openai_api_key,
            openai_organization=openai_organization,
            temperature=temperature,
            max_tokens=-1,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=num_completions,
            batch_size=batch_size,
            max_retries=max_retries,
        )
        self.model_max_tokens = TOKEN_LIMITS[model]
        self.model_type = MODEL_TYPES[model]
        self.openai_api_key = openai_api_key

    def get_output(self, prompt: str | Prompt) -> str:
        """Generate a single output from the LLM.

        Arguments:
            prompt: The prompt(s) to use for the LLM.

        Returns:
            The output of the LLM.
        """
        output = self._langchain_model(prompt)

    def __str__(self) -> str:
        """Return a string representation of the LLM."""
        return self.model
