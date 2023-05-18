from janus import Translator
from janus.utils.logger import create_logger

log = create_logger(__name__)


translator = Translator("gpt-3.5-turbo", "fortran", "python", "3.10")

translator.translate("elmfire/build/source", "/tmp/translated")
