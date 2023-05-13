"""
Package
-------
This will be used in CI to make sure that we can import all of the packages/modules in the
installed package.
"""
import sys
import traceback
from importlib import import_module
from modulefinder import ModuleFinder

import janus
from janus import llm, utils

# Find all of the submodules
finder = ModuleFinder()
sub_modules = ["janus." + m for m in finder.find_all_submodules(janus)]
sub_modules += ["janus.llm." + m for m in finder.find_all_submodules(llm)]
sub_modules += ["janus.utils." + m for m in finder.find_all_submodules(utils)]

# Import all of the found submodules
for module in sub_modules:
    try:
        import_module(module)
    except ModuleNotFoundError:
        traceback.print_exc()
        sys.exit(1)

print("\nSuccessfully imported modules!")
