import warnings

from langchain_core._api.deprecation import LangChainDeprecationWarning

from janus.converter.translate import Translator
from janus.metrics import *  # noqa: F403

__version__ = "4.0.0"

# Ignoring a deprecation warning from langchain_core that I can't seem to hunt down
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
