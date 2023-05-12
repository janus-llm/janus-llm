import time
from typing import Dict, List

import openai

from logger import create_logger


log = create_logger(__name__)


MODEL_TYPES: Dict[str, str] = {
    "gpt-3.5-turbo": "chat-gpt",
    "text-davinci-003": "gpt-3",
    "text-curie-001": "gpt-3",
    "text-babbage-001": "gpt-3",
    "text-ada-001": "gpt-3",
}


class LLM:
    """A class to interact with the OpenAI LLMs."""

    def __init__(
        self,
        model: str,
        open_ai_api_key: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        max_tokens: int = 1024,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
    ) -> None:
        """Initialize the LLM.

        Arguments:
            model: The model to use for the LLM.
            open_ai_api_key: The OpenAI API key to use for the LLM.

        Chat GPT Arguments:
            temperature: The temperature to use for the LLM.
            top_p: The top p to use for the LLM.
            n: The number of outputs to generate per prompt.
            stream: Whether to stream the output.
            stop: A list of strings to stop the LLM from generating.
            max_tokens: The maximum number of tokens to generate.
            presence_penalty: The presence penalty to use for the LLM.
            frequency_penalty: The frequency penalty to use for the LLM.
            logit_bias: A dictionary of tokens to bias the output towards.

        See [here](https://platform.openai.com/docs/api-reference/chat/create) for more
        documentation on each variable.

        GPT-3 Arguments:
            suffix: The suffix to use for the LLM.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature to use for the LLM.
            top_p: The top p to use for the LLM.
            n: The number of outputs to generate.
            stream: Whether to stream the output.
            logprobs: The number of logprobs to return.
            echo: Whether to echo the prompt.
            stop: A list of strings to stop the LLM from generating.
            presence_penalty: The presence penalty to use for the LLM.
            frequency_penalty: The frequency penalty to use for the LLM.
            best_of: The number of best outputs to return.
            logit_bias: A dictionary of tokens to bias the output towards.

        Raises:
            ValueError: If the model is not supported.
        """
        self.model = model
        if model not in list(MODEL_TYPES.keys()):
            raise ValueError(
                f"Model {model} not supported. Select from one of the "
                f"following: {list(MODEL_TYPES.keys())}"
            )
        self.model_type = MODEL_TYPES[model]
        self.open_ai_api_key = open_ai_api_key
        openai.api_key = open_ai_api_key

        # Set these to null if None so that they are not passed to the API
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty

    def get_output(self, prompt: str | List[Dict[str, str]]) -> str:
        """Generate a single output from the LLM.

        Arguments:
            prompt: The prompt(s) to use for the LLM.

        Returns:
            The output of the LLM.
        """
        try:
            if self.model_type == "chat-gpt":
                return self._get_output_chat_gpt(prompt)
            else:
                return self._get_output_gpt_3(prompt)
        except openai.error.RateLimitError:
            log.error(
                "OpenAI API rate limit exceeded. Waiting 1 minute and trying again."
            )
            time.sleep(60)
            output = self.get_output(prompt)
            return output
        except openai.error.Timeout:
            log.error("OpenAI API timeout. Waiting 1 minute and trying again.")
            time.sleep(60)
            output = self.get_output(prompt)
            return output

    def _get_output_chat_gpt(self, messages: List[Dict[str, str]]) -> str:
        """Generate a single output from a 'chat-gpt' LLM.

        Arguments:
            messages: A list of messages to use for the LLM.

        Returns:
            The output of the 'chat-gpt' LLM.
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
        )

        output = response["choices"][0]["message"]["content"]

        return output

    def _get_output_gpt_3(self, prompt: str) -> str:
        """Generate a single output from the LLM.

        Arguments:
            prompt: The prompt to use for the LLM.

        Returns:
            The output of the LLM.
        """
        output = openai.Completion.create(
            model=self.model,
            suffix=self.suffix,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )

        return output["choices"][0]["text"]

    def get_output_batch(
        self, prompts: List[str] | List[List[Dict[str, str]]]
    ) -> List[str]:
        """Generate a batch of outputs from the LLM.

        Chat GPT Arguments:
            prompts: The prompts to use for the LLM.

        Returns:
            The outputs of the LLM.
        """
        log.info(f"Generating {len(prompts)} outputs with the following parameters: ")
        log.info(f"Model: {self.model}")
        log.info(f"Temperature: {self.temperature}")
        log.info(f"Top P: {self.top_p}")
        log.info(f"Max Tokens: {self.max_tokens}")
        log.info(f"Presence Penalty: {self.presence_penalty}")
        log.info(f"Frequency Penalty: {self.frequency_penalty}")

        outputs = []

        for prompt in prompts:
            if self.model_type == "chat-gpt":
                if not isinstance(prompt, list):
                    raise ValueError(
                        "Prompts must be a list of messages for " "chat-gpt models."
                    )
                outputs.append(self._get_output_chat_gpt(prompt))
            else:
                if not isinstance(prompt, str):
                    raise ValueError(
                        "Prompts must be a string for non-chat-gpt " "models."
                    )
                outputs.append(self._get_output_gpt_3(prompt))

        return outputs

    def __str__(self) -> str:
        """Return a string representation of the LLM."""
        return self.model