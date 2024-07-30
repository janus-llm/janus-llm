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
from janus import embedding, language, llm, metrics, parsers, prompts, utils
from janus.language import binary, mumps, treesitter

# Find all of the submodules
finder = ModuleFinder()
sub_modules = ["janus." + m for m in finder.find_all_submodules(janus)]
sub_modules += ["janus.llm." + m for m in finder.find_all_submodules(llm)]
sub_modules += ["janus.utils." + m for m in finder.find_all_submodules(utils)]
sub_modules += ["janus.metrics." + m for m in finder.find_all_submodules(metrics)]
sub_modules += ["janus.parsers." + m for m in finder.find_all_submodules(parsers)]
sub_modules += ["janus.prompts." + m for m in finder.find_all_submodules(prompts)]
sub_modules += ["janus.embedding." + m for m in finder.find_all_submodules(embedding)]
sub_modules += ["janus.language." + m for m in finder.find_all_submodules(language)]
sub_modules += ["janus.language.binary." + m for m in finder.find_all_submodules(binary)]
sub_modules += ["janus.language.mumps." + m for m in finder.find_all_submodules(mumps)]
sub_modules += [
    "janus.language.treesitter." + m for m in finder.find_all_submodules(treesitter)
]

# Import all of the found submodules
for module in sub_modules:
    try:
        import_module(module)
    except ModuleNotFoundError:
        traceback.print_exc()
        sys.exit(1)

print("\nSuccessfully imported modules!")
