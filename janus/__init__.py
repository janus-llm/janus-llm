import warnings

from langchain_core._api.deprecation import LangChainDeprecationWarning

from .converter.translate import Translator
from .metrics import *  # noqa: F403

__version__ = "3.0.1"

# Ignoring a deprecation warning from langchain_core that I can't seem to hunt down
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
