# Introduction

Janus LLM (`janus-llm`) allows users to parse and chunk over 100 programming languages and embed that information into a [chroma](trychroma.com) vector database for retrieval augmented generation (RAG).

[GitHub Page](https://github.com/janus-llm/janus-llm)

## Installing

### Installing via Pip

```shell
pip install janus-llm
```

### Installing from Source

Clone the repository:

```shell
git clone git@github.com:janus-llm/janus-llm.git
```

Then, install the requirements:

```shell
curl -sSkL https://install.python-poetry.org | python -
export PATH=$PATH:$HOME/.local/bin
poetry install --no-dev
```

## Using as a CLI

TODO


## Supported Languages

Below is a list of supported languages, linked to their corresponding tree-sitter grammar repository (if it exists):

- [ada](https://github.com/briot/tree-sitter-ada)
- [agda](https://github.com/tree-sitter/tree-sitter-agda)
- [x86asm](https://github.com/bearcove/tree-sitter-x86asm)
- [bash](https://github.com/tree-sitter/tree-sitter-bash)
- binary (must have [Ghidra](https://github.com/NationalSecurityAgency/ghidra) installed)
- [beancount](https://github.com/zwpaper/tree-sitter-beancount)
- [bigquery](https://github.com/takegue/tree-sitter-sql-bigquery)
- [c](https://github.com/tree-sitter/tree-sitter-c)
- [capnp](https://github.com/amaanq/tree-sitter-capnp)
- [cmake](https://github.com/uyha/tree-sitter-cmake)
- [comment](https://github.com/stsewd/tree-sitter-comment)
- [commonlisp](https://github.com/theHamsta/tree-sitter-commonlisp)
- [config](https://github.com/metio/tree-sitter-ssh-client-config)
- [css](https://github.com/tree-sitter/tree-sitter-css)
- [cuda](https://github.com/theHamsta/tree-sitter-cuda)
- [d](https://github.com/gdamore/tree-sitter-d)
- [dart](https://github.com/UserNobody14/tree-sitter-dart)
- [dockerfile](https://github.com/camdencheek/tree-sitter-dockerfile)
- [dot](https://github.com/rydesun/tree-sitter-dot)
- [elisp](https://github.com/Wilfred/tree-sitter-elisp)
- [elixir](https://github.com/elixir-lang/tree-sitter-elixir)
- [elm](https://github.com/elm-tooling/tree-sitter-elm)
- [eno](https://github.com/eno-lang/tree-sitter-eno)
- [erlang](https://github.com/WhatsApp/tree-sitter-erlang)
- [fennel](https://github.com/travonted/tree-sitter-fennel)
- [fish](https://github.com/ram02z/tree-sitter-fish)
- [formula](https://github.com/siraben/tree-sitter-formula)
- [fortran](https://github.com/stadelmanma/tree-sitter-fortran)
- [gitattributes](https://github.com/ObserverOfTime/tree-sitter-gitattributes)
- [gitignore](https://github.com/shunsambongi/tree-sitter-gitignore)
- [gleam](https://github.com/gleam-lang/tree-sitter-gleam)
- [glsl](https://github.com/theHamsta/tree-sitter-glsl)
- [go](https://github.com/tree-sitter/tree-sitter-go)
- [graphql](https://github.com/bkegley/tree-sitter-graphql)
- [hack](https://github.com/slackhq/tree-sitter-hack)
- [haskell](https://github.com/tree-sitter/tree-sitter-haskell)
- [hcl](https://github.com/MichaHoffmann/tree-sitter-hcl)
- [html](https://github.com/tree-sitter/tree-sitter-html)
- [java](https://github.com/tree-sitter/tree-sitter-java)
- [javascript](https://github.com/tree-sitter/tree-sitter-javascript)
- [jq](https://github.com/flurie/tree-sitter-jq)
- [json](https://github.com/tree-sitter/tree-sitter-json)
- [json5](https://github.com/Joakker/tree-sitter-json5)
- [julia](https://github.com/tree-sitter/tree-sitter-julia)
- [kotlin](https://github.com/fwcd/tree-sitter-kotlin)
- [lalrpop](https://github.com/traxys/tree-sitter-lalrpop)
- [latex](https://github.com/latex-lsp/tree-sitter-latex)
- [lean](https://github.com/Julian/tree-sitter-lean)
- [llvm](https://github.com/benwilliamgraham/tree-sitter-llvm)
- [lua](https://github.com/Azganoth/tree-sitter-lua)
- [m68k](https://github.com/grahambates/tree-sitter-m68k)
- [markdown](https://github.com/ikatyang/tree-sitter-markdown)
- [matlab](https://github.com/acristoffers/tree-sitter-matlab)
- [meson](https://github.com/staysail/tree-sitter-meson)
- mumps
- [nix](https://github.com/cstrahan/tree-sitter-nix)
- [objc](https://github.com/jiyee/tree-sitter-objc)
- [ocaml](https://github.com/tree-sitter/tree-sitter-ocaml)
- [org](https://github.com/milisims/tree-sitter-org)
- [pascal](https://github.com/Isopod/tree-sitter-pascal)
- [perl](https://github.com/tree-sitter-perl/tree-sitter-perl)
- [pgn](https://github.com/rolandwalker/tree-sitter-pgn)
- [php](https://github.com/tree-sitter/tree-sitter-php)
- [pod](https://github.com/tree-sitter-perl/tree-sitter-pod)
- [powershell](https://github.com/PowerShell/tree-sitter-PowerShell)
- [proto](https://github.com/mitchellh/tree-sitter-proto)
- pseudocode
- [python](https://github.com/tree-sitter/tree-sitter-python)
- [qmljs](https://github.com/yuja/tree-sitter-qmljs)
- [r](https://github.com/r-lib/tree-sitter-r)
- [racket](https://github.com/6cdh/tree-sitter-racket)
- [rasi](https://github.com/Fymyte/tree-sitter-rasi)
- [re2c](https://github.com/alemuller/tree-sitter-re2c)
- [regex](https://github.com/tree-sitter/tree-sitter-regex)
- [rego](https://github.com/FallenAngel97/tree-sitter-rego)
- [rst](https://github.com/stsewd/tree-sitter-rst)
- [ruby](https://github.com/tree-sitter/tree-sitter-ruby)
- [rust](https://github.com/tree-sitter/tree-sitter-rust)
- [scala](https://github.com/tree-sitter/tree-sitter-scala)
- [scheme](https://github.com/6cdh/tree-sitter-scheme)
- [scss](https://github.com/serenadeai/tree-sitter-scss)
- [sexp](https://github.com/AbstractMachinesLab/tree-sitter-sexp)
- [sfapex](https://github.com/aheber/tree-sitter-sfapex)
- [smali](https://github.com/amaanq/tree-sitter-smali)
- [sourcepawn](https://github.com/nilshelmig/tree-sitter-sourcepawn)
- [sparql](https://github.com/BonaBeavis/tree-sitter-sparql)
- [sql](https://github.com/m-novikov/tree-sitter-sql)
- [sqlite](https://github.com/dhcmrlchtdj/tree-sitter-sqlite)
- [svelte](https://github.com/Himujjal/tree-sitter-svelte)
- [swift](https://github.com/alex-pinkus/tree-sitter-swift)
- [systemrdl](https://github.com/SystemRDL/tree-sitter-systemrdl)
- [template](https://github.com/tree-sitter/tree-sitter-embedded-template)
- text
- [thrift](https://github.com/duskmoon314/tree-sitter-thrift)
- [toml](https://github.com/ikatyang/tree-sitter-toml)
- [turtle](https://github.com/BonaBeavis/tree-sitter-turtle)
- [twig](https://github.com/gbprod/tree-sitter-twig)
- [typescript](https://github.com/tree-sitter/tree-sitter-typescript)
- [verilog](https://github.com/tree-sitter/tree-sitter-verilog)
- [vhdl](https://github.com/alemuller/tree-sitter-vhdl)
- [vue](https://github.com/ikatyang/tree-sitter-vue)
- [wasm](https://github.com/wasm-lsp/tree-sitter-wasm)
- [wgsl](https://github.com/mehmetoguzderin/tree-sitter-wgsl)
- [yaml](https://github.com/ikatyang/tree-sitter-yaml)
- [yang](https://github.com/Hubro/tree-sitter-yang)
- [zig](https://github.com/maxxnino/tree-sitter-zig)
