from pathlib import Path

from janus.language.fortran import FortranSplitter
from janus.utils.logger import create_logger

log = create_logger(__name__)

splitter = FortranSplitter()

components = splitter.split(Path("elmfire/build/source/elmfire_ignition.f90"))

log.info("DONE")
