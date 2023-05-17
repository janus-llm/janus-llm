from pathlib import Path
from typing import List

from janus.language.fortran import FortranSplitter
from janus.language.block import File
from janus.utils.logger import create_logger

log = create_logger(__name__)

splitter = FortranSplitter()

files: List[File] = []

for file in Path("elmfire/build/source").glob("*.f90"):
    log.info(f"Splitting {file}")
    files.append(splitter.split(file))

log.info("DONE")
