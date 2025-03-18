import json
import os
from pathlib import Path
from typing import Callable, Protocol, TypeVar

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI

from janus.llm.model_callbacks import COST_PER_1K_TOKENS, azure_model_reroutes
from janus.prompts.prompt import (
    ChatGptPromptEngine,
    ClaudePromptEngine,
    CoherePromptEngine,
    GranitePromptEngine,
    Llama2PromptEngine,
    Llama3PromptEngine,
    MistralPromptEngine,
    PromptEngine,
    TitanPromptEngine,
)
from janus.utils.logger import create_logger

log = create_logger(__name__)

model_types = [
    "ModelType",
    AzureChatOpenAI,
    HuggingFaceTextGenInference,
]

try:
    from boto3 import client
    from botocore.config import Config
    from langchain_community.chat_models import BedrockChat
    from langchain_community.llms.bedrock import Bedrock

    model_types += [
        Bedrock,
        BedrockChat,
    ]
except ImportError:
    log.warning(
        "Could not import LangChain's Bedrock Client. If you would like to use Bedrock "
        "models, please install LangChain's Bedrock Client by running 'pip install "
        "janus-llm[bedrock]' or poetry install -E bedrock."
    )

try:
    from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

    model_types += [HuggingFacePipeline]
except ImportError:
    log.warning(
        "Could not import LangChain's HuggingFace Pipeline Client. If you would like to "
        "use HuggingFace models, please install LangChain's HuggingFace Pipeline Client "
        "by running 'pip install janus-llm[hf-local]' or poetry install -E hf-local."
    )


ModelType = TypeVar(*model_types)

MODEL_TYPE_CONSTRUCTORS: dict[str, ModelType] = {
    # "OpenAI": ChatOpenAI,
    "HuggingFace": HuggingFaceTextGenInference,
    "Azure": AzureChatOpenAI,
}

try:
    MODEL_TYPE_CONSTRUCTORS["Bedrock"] = Bedrock
    MODEL_TYPE_CONSTRUCTORS["BedrockChat"] = BedrockChat
    MODEL_TYPE_CONSTRUCTORS["Granite"] = BedrockChat
except NameError:
    log.warning(
        "Could not import LangChain's Bedrock Client. If you would like to use Bedrock "
        "models, please install LangChain's Bedrock Client by running 'pip install "
        "janus-llm[bedrock]' or poetry install -E bedrock."
    )

try:
    MODEL_TYPE_CONSTRUCTORS["HuggingFaceLocal"] = HuggingFacePipeline
except NameError:
    log.warning(
        "Could not import LangChain's HuggingFace Pipeline Client. If you would like to "
        "use HuggingFace models, please install LangChain's HuggingFace Pipeline Client "
        "by running 'pip install janus-llm[hf-local]' or poetry install -E hf-local."
    )


class JanusModelProtocol(Protocol):
    model_id: str
    model_type_name: str
    token_limit: int
    input_token_cost: float
    output_token_cost: float
    prompt_engine: type[PromptEngine]

    def get_num_tokens(self, text: str) -> int:
        ...


class JanusModel(Runnable, JanusModelProtocol):
    ...


load_dotenv()

openai_models = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]
azure_models = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-3.5-turbo-16k",
]
claude_models = [
    "bedrock-claude-v2",
    "bedrock-claude-instant-v1",
    "bedrock-claude-haiku",
    "bedrock-claude-sonnet",
    "bedrock-claude-sonnet-3.5",
    "bedrock-claude-sonnet-3.5-v2",
    "bedrock-claude-haiku-3.5",
    "bedrock-claude-sonnet-3.7",
]
llama2_models = [
    "bedrock-llama2-70b",
    "bedrock-llama2-70b-chat",
    "bedrock-llama2-13b",
    "bedrock-llama2-13b-chat",
    "bedrock-llama3-1-405b-instruct",
    "bedrock-llama3-8b-instruct",
    "bedrock-llama3-70b-instruct",
    "bedrock-llama3-3-70b-instruct",
]
llama3_models = [
    "bedrock-llama3-8b-instruct",
    "bedrock-llama3-70b-instruct",
    "bedrock-llama3-3-70b-instruct",
]
titan_models = [
    "bedrock-titan-text-lite",
    "bedrock-titan-text-express",
    "bedrock-jurassic-2-mid",
    "bedrock-jurassic-2-ultra",
]
nova_models = [
    "bedrock-nova-lite",
    "bedrock-nova-micro",
    "bedrock-nova-pro",
]
cohere_models = [
    "bedrock-command-r-plus",
]
mistral_models = [
    "bedrock-mistral-7b-instruct",
    "bedrock-mistral-large-32k",
    "bedrock-mistral-large-131k",
    "bedrock-mixtral",
]
granite_models = [
    "bedrock-granite-3b-code-instruct",
]
bedrock_models = [
    *claude_models,
    *llama2_models,
    *llama3_models,
    *titan_models,
    *cohere_models,
    *mistral_models,
]
all_models = [*azure_models, *bedrock_models, *granite_models]


MODEL_PROMPT_ENGINES: dict[str, Callable[..., PromptEngine]] = {
    # **{m: ChatGptPromptEngine for m in openai_models},
    **{m: ChatGptPromptEngine for m in azure_models},
    **{m: ClaudePromptEngine for m in claude_models},
    **{m: Llama2PromptEngine for m in llama2_models},
    **{m: Llama3PromptEngine for m in llama3_models},
    **{m: TitanPromptEngine for m in titan_models},
    **{m: CoherePromptEngine for m in cohere_models},
    **{m: MistralPromptEngine for m in mistral_models},
    **{m: GranitePromptEngine for m in granite_models},
}

MODEL_ID_TO_LONG_ID = {
    # **{m: mr for m, mr in openai_model_reroutes.items()},
    **{m: mr for m, mr in azure_model_reroutes.items()},
    "bedrock-claude-v2": "anthropic.claude-v2",
    "bedrock-claude-instant-v1": "anthropic.claude-instant-v1",
    "bedrock-claude-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "bedrock-claude-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "bedrock-claude-sonnet-3.5": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "bedrock-claude-sonnet-3.5-v2": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "bedrock-claude-haiku-3.5": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "bedrock-claude-sonnet-3.7": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "bedrock-llama2-70b": "meta.llama2-70b-v1",
    "bedrock-llama2-70b-chat": "meta.llama2-70b-chat-v1",
    "bedrock-llama2-13b": "meta.llama2-13b-chat-v1",
    "bedrock-llama2-13b-chat": "meta.llama2-13b-v1",
    "bedrock-llama3-8b-instruct": "meta.llama3-8b-instruct-v1:0",
    "bedrock-llama3-70b-instruct": "meta.llama3-70b-instruct-v1:0",
    "bedrock-llama3-1-405b-instruct": "us.meta.llama3-1-405b-instruct-v1:0",
    "bedrock-llama3-3-70b-instruct": "us.meta.llama3-3-70b-instruct-v1:0",
    "bedrock-llama3-3-70b-instruct": "us.meta.llama3-3-70b-instruct-v1:0",
    "bedrock-nova-lite": "amazon.nova-lite-v1:0",
    "bedrock-nova-micro": "amazon.nova-micro-v1:0",
    "bedrock-nova-pro": "amazon.nova-pro-v1:0",
    "bedrock-titan-text-lite": "amazon.titan-text-lite-v1",
    "bedrock-titan-text-express": "amazon.titan-text-express-v1",
    "bedrock-jurassic-2-mid": "ai21.j2-mid-v1",
    "bedrock-jurassic-2-ultra": "ai21.j2-ultra-v1",
    "bedrock-command-r-plus": "cohere.command-r-plus-v1:0",
    "bedrock-mixtral": "mistral.mixtral-8x7b-instruct-v0:1",
    "bedrock-mistral-7b-instruct": "mistral.mistral-7b-instruct-v0:2",
    "bedrock-mistral-large-32k": "mistral.mistral-large-2402-v1:0",
    "bedrock-mistral-large-131k": "mistral.mistral-large-2407-v1:0",
    "bedrock-granite-3b-code-instruct": (
        "arn:aws:bedrock:us-east-1:851725275899:imported-model/shp03b13vje5"
    ),
}

MODEL_DEFAULT_ARGUMENTS: dict[str, dict[str, str]] = {
    k: (dict(model_name=k) if k in openai_models else dict(model_id=v))
    for k, v in MODEL_ID_TO_LONG_ID.items()
}

DEFAULT_MODELS = list(MODEL_DEFAULT_ARGUMENTS.keys())

MODEL_CONFIG_DIR = Path.home().expanduser() / ".janus" / "llm"

MODEL_TYPES: dict[str, PromptEngine] = {
    # **{m: "OpenAI" for m in openai_models},
    **{m: "Azure" for m in azure_models},
    **{m: "BedrockChat" for m in bedrock_models},
    **{m: "Granite" for m in granite_models},
}

TOKEN_LIMITS: dict[str, int] = {
    "gpt-4-32k": 32_768,
    "gpt-4-0613": 8192,
    "gpt-4-1106-preview": 128_000,
    "gpt-4-0125-preview": 128_000,
    "gpt-4o-2024-05-13": 128_000,
    "gpt-4o-2024-08-06": 128_000,
    "gpt-4o-mini": 128_000,
    "gpt-3.5-turbo-0125": 16_384,
    "gpt35-turbo-16k": 16_384,
    "text-embedding-ada-002": 8191,
    "gpt4all": 16_384,
    "anthropic.claude-v2": 100_000,
    "anthropic.claude-instant-v1": 100_000,
    "anthropic.claude-3-haiku-20240307-v1:0": 248_000,
    "anthropic.claude-3-sonnet-20240229-v1:0": 248_000,
    "anthropic.claude-3-5-sonnet-20240620-v1:0": 200_000,
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0": 200_000,
    "us.anthropic.claude-3-5-haiku-20241022-v1:0": 200_000,
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0": 200_000,
    "meta.llama2-70b-v1": 4096,
    "meta.llama2-70b-chat-v1": 4096,
    "meta.llama2-13b-chat-v1": 4096,
    "meta.llama2-13b-v1": 4096,
    "meta.llama3-8b-instruct-v1:0": 8000,
    "meta.llama3-70b-instruct-v1:0": 8000,
    "us.meta.llama3-1-405b-instruct-v1:0": 120_000,
    "us.meta.llama3-3-70b-instruct-v1:0": 128_000,
    "us.meta.llama3-3-70b-instruct-v1:0": 128_000,
    "amazon.nova-lite-v1:0": 300_000,
    "amazon.nova-micro-v1:0": 128_000,
    "amazon.nova-pro-v1:0": 300_000,
    "amazon.titan-text-lite-v1": 4096,
    "amazon.titan-text-express-v1": 8192,
    "ai21.j2-mid-v1": 8192,
    "ai21.j2-ultra-v1": 8192,
    "cohere.command-r-plus-v1:0": 128_000,
    "mistral.mixtral-8x7b-instruct-v0:1": 32_000,
    "mistral.mistral-7b-instruct-v0:2": 32_000,
    "mistral.mistral-large-2402-v1:0": 32_000,
    "mistral.mistral-large-2407-v1:0": 131_000,
    "arn:aws:bedrock:us-east-1:851725275899:imported-model/shp03b13vje5": 128_000,
}


def get_available_model_names() -> list[str]:
    avaialable_models = []
    for file in MODEL_CONFIG_DIR.iterdir():
        if file.is_file():
            avaialable_models.append(MODEL_CONFIG_DIR.stem)
    return avaialable_models


def load_model(model_id) -> JanusModel:
    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_config_file = MODEL_CONFIG_DIR / f"{model_id}.json"

    if model_config_file.exists():
        log.info(f"Loading {model_id} from {model_config_file}.")
        with open(model_config_file, "r") as f:
            model_config = json.load(f)
        model_type_name = model_config["model_type"]
        model_id = model_config["model_id"]
        model_args = model_config["model_args"]
        token_limit = model_config["token_limit"]
        input_token_cost = model_config["model_cost"]["input"]
        output_token_cost = model_config["model_cost"]["output"]
        input_token_proportion = model_config["input_token_proportion"]

    elif model_id in DEFAULT_MODELS:
        model_id = model_id
        model_long_id = MODEL_ID_TO_LONG_ID[model_id]
        model_type_name = MODEL_TYPES[model_id]
        model_args = MODEL_DEFAULT_ARGUMENTS[model_id]

        token_limit = 0
        input_token_cost = 0.0
        output_token_cost = 0.0
        input_token_proportion = 0.4
        if model_long_id in TOKEN_LIMITS:
            token_limit = TOKEN_LIMITS[model_long_id]
        if model_long_id in COST_PER_1K_TOKENS:
            token_limits = COST_PER_1K_TOKENS[model_long_id]
            input_token_cost = token_limits["input"]
            output_token_cost = token_limits["output"]

    else:
        model_list = "\n\t".join(DEFAULT_MODELS)
        message = (
            f"Model {model_id} not found in user-defined model directory "
            f"({MODEL_CONFIG_DIR}), and is not a default model. Valid default "
            f"models:\n\t{model_list}\n"
            f"To use a custom model, first run `janus llm add`."
        )
        log.error(message)
        raise ValueError(message)

    if model_type_name == "HuggingFaceLocal":
        model = HuggingFacePipeline.from_model_id(
            model_id=model_id,
            task="text-generation",
            model_kwargs=model_args,
        )
        model_args.update(pipeline=model.pipeline)

    elif model_type_name == "OpenAI":
        model_args.update(
            openai_api_key=str(os.getenv("OPENAI_API_KEY")),
        )
        # log.warning("Do NOT use this model in sensitive environments!")
        # log.warning("If you would like to cancel, please press Ctrl+C.")
        # log.warning("Waiting 10 seconds...")
        # Give enough time for the user to read the warnings and cancel
        # time.sleep(10)
        raise DeprecationWarning("OpenAI models are no longer supported.")

    elif model_type_name == "Azure":
        model_args.update(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-02-01"),
            azure_deployment=model_id,
            request_timeout=3600,
            max_tokens=4096,
        )

    elif model_type_name == "Granite":
        # This is a workaround for bedrock logic, which determines output keys by provider
        # The API does not yet list IBM, but IBM models use the same key ('generation')
        #  as Meta models do
        model_args.update(provider="meta")

    elif model_type_name.startswith("Bedrock"):
        config = Config(read_timeout=1000)
        cli = client(service_name="bedrock-runtime", config=config)
        model_args.update(
            client=cli,
        )

    # log.info(f"Checking model provider: {model_long_id}")
    # if model_long_id.startswith("us.meta"):
    #     log.info("Changing model provider")
    #     model_args.update(provider="meta")
    # elif model_long_id.startswith("us.anthropic"):
    #     log.info("Changing model provider")
    #     model_args.update(provider="anthropic")

    # if model_id == "bedrock-claude-sonnet-3.7":
    #     model_args.update(
    #         model_kwargs=dict(
    #             max_tokens=128_000,
    #             # thinking=dict(
    #             #     type="enabled",
    #             #     budget_tokens=4_000,
    #             # )
    #         ),
    #         # timeout=1000,
    #     )

    model_type = MODEL_TYPE_CONSTRUCTORS[model_type_name]
    prompt_engine = MODEL_PROMPT_ENGINES[model_id]

    class JanusModel(model_type):
        model_id: str
        # model_name is for LangChain compatibility
        # It searches for `self.model_name` when counting tokens
        model_name: str
        short_model_id: str
        model_type_name: str
        token_limit: int
        input_token_proportion: float
        input_token_cost: float
        output_token_cost: float
        prompt_engine: type[PromptEngine]

    model_args.update(
        model_id=MODEL_ID_TO_LONG_ID[model_id],
        model_name=model_id,  # This is for LangChain compatibility
        short_model_id=model_id,
    )

    return JanusModel(
        model_type_name=model_type_name,
        token_limit=token_limit,
        input_token_cost=input_token_cost,
        output_token_cost=output_token_cost,
        input_token_proportion=input_token_proportion,
        prompt_engine=prompt_engine,
        **model_args,
    )
