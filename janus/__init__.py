import warnings

from langchain_core._api.deprecation import LangChainDeprecationWarning

from .metrics import *  # noqa: F403
from .translate import Translator

__version__ = "2.2.0"

# Ignoring a deprecation warning from langchain_core that I can't seem to hunt down
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
