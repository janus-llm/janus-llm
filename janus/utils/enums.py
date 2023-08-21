from typing import Dict, Tuple

CUSTOM_SPLITTERS: Tuple[str, ...] = ("mumps",)

LANGUAGES: Dict[str, Dict[str, str]] = {
    "ada": {
        "comment": "--",
        "suffix": "adb",
        "url": "https://github.com/briot/tree-sitter-ada",
    },
    "agda": {
        "comment": "--",
        "suffix": "agda",
        "url": "https://github.com/tree-sitter/tree-sitter-agda",
    },
    "bash": {
        "comment": "#",
        "suffix": "sh",
        "url": "https://github.com/tree-sitter/tree-sitter-bash",
    },
    "beancount": {
        "comment": ";",
        "suffix": "beancount",
        "url": "https://github.com/zwpaper/tree-sitter-beancount",
    },
    "bigquery": {
        "comment": "--",
        "suffix": "sql",
        "url": "https://github.com/takegue/tree-sitter-sql-bigquery",
    },
    "c": {
        "comment": "//",
        "suffix": "c",
        "url": "https://github.com/tree-sitter/tree-sitter-c",
    },
    "capnp": {
        "comment": "#",
        "suffix": "capnp",
        "url": "https://github.com/amaanq/tree-sitter-capnp",
    },
    "cmake": {
        "comment": "#",
        "suffix": "cmake",
        "url": "https://github.com/uyha/tree-sitter-cmake",
    },
    "comment": {
        "comment": "#",
        "suffix": "comment",
        "url": "https://github.com/stsewd/tree-sitter-comment",
    },
    "commonlisp": {
        "comment": ";;",
        "suffix": "lisp",
        "url": "https://github.com/theHamsta/tree-sitter-commonlisp",
    },
    "config": {
        "comment": "#",
        "suffix": None,
        "url": "https://github.com/metio/tree-sitter-ssh-client-config",
    },
    "css": {
        "comment": "/*",
        "suffix": "css",
        "url": "https://github.com/tree-sitter/tree-sitter-css",
    },
    "cuda": {
        "comment": "//",
        "suffix": "cu",
        "url": "https://github.com/theHamsta/tree-sitter-cuda",
    },
    "d": {
        "comment": "//",
        "suffix": "d",
        "url": "https://github.com/gdamore/tree-sitter-d",
    },
    "dart": {
        "comment": "//",
        "suffix": "dart",
        "url": "https://github.com/UserNobody14/tree-sitter-dart",
    },
    "dockerfile": {
        "comment": "#",
        "suffix": "Dockerfile",
        "url": "https://github.com/camdencheek/tree-sitter-dockerfile",
    },
    "dot": {
        "comment": "//",
        "suffix": "dot",
        "url": "https://github.com/rydesun/tree-sitter-dot",
    },
    "elisp": {
        "comment": ";;",
        "suffix": "el",
        "url": "https://github.com/Wilfred/tree-sitter-elisp",
    },
    "elixir": {
        "comment": "#",
        "suffix": "ex",
        "url": "https://github.com/elixir-lang/tree-sitter-elixir",
    },
    "elm": {
        "comment": "--",
        "suffix": "elm",
        "url": "https://github.com/elm-tooling/tree-sitter-elm",
    },
    "eno": {
        "comment": "#",
        "suffix": "eno",
        "url": "https://github.com/eno-lang/tree-sitter-eno",
    },
    "erlang": {
        "comment": "%",
        "suffix": "erl",
        "url": "https://github.com/WhatsApp/tree-sitter-erlang",
    },
    "fennel": {
        "comment": ";",
        "suffix": "fnl",
        "url": "https://github.com/travonted/tree-sitter-fennel",
    },
    "fish": {
        "comment": "#",
        "suffix": "fish",
        "url": "https://github.com/ram02z/tree-sitter-fish",
    },
    "formula": {
        "comment": ";",
        "suffix": "formula",
        "url": "https://github.com/siraben/tree-sitter-formula",
    },
    "fortran": {
        "comment": "!",
        "suffix": "f90",
        "url": "https://github.com/stadelmanma/tree-sitter-fortran",
    },
    "gitattributes": {
        "comment": "#",
        "suffix": "gitattributes",
        "url": "https://github.com/ObserverOfTime/tree-sitter-gitattributes",
    },
    "gitignore": {
        "comment": "#",
        "suffix": "gitignore",
        "url": "https://github.com/shunsambongi/tree-sitter-gitignore",
    },
    "gleam": {
        "comment": "//",
        "suffix": "gleam",
        "url": "https://github.com/gleam-lang/tree-sitter-gleam",
    },
    "glsl": {
        "comment": "//",
        "suffix": "glsl",
        "url": "https://github.com/theHamsta/tree-sitter-glsl",
    },
    "go": {
        "comment": "//",
        "suffix": "go",
        "url": "https://github.com/tree-sitter/tree-sitter-go",
    },
    "graphql": {
        "comment": "#",
        "suffix": "graphql",
        "url": "https://github.com/bkegley/tree-sitter-graphql",
    },
    "hack": {
        "comment": "//",
        "suffix": "hack",
        "url": "https://github.com/slackhq/tree-sitter-hack",
    },
    "haskell": {
        "comment": "--",
        "suffix": "hs",
        "url": "https://github.com/tree-sitter/tree-sitter-haskell",
    },
    "hcl": {
        "comment": "#",
        "suffix": "hcl",
        "url": "https://github.com/MichaHoffmann/tree-sitter-hcl",
    },
    "html": {
        "comment": "<!--",
        "suffix": "html",
        "url": "https://github.com/tree-sitter/tree-sitter-html",
    },
    "java": {
        "comment": "//",
        "suffix": "java",
        "url": "https://github.com/tree-sitter/tree-sitter-java",
    },
    "javascript": {
        "comment": "//",
        "suffix": "js",
        "url": "https://github.com/tree-sitter/tree-sitter-javascript",
    },
    "jq": {
        "comment": "#",
        "suffix": "jq",
        "url": "https://github.com/flurie/tree-sitter-jq",
    },
    "json": {
        "comment": "//",
        "suffix": "json",
        "url": "https://github.com/tree-sitter/tree-sitter-json",
    },
    "json5": {
        "comment": "//",
        "suffix": "json5",
        "url": "https://github.com/Joakker/tree-sitter-json5",
    },
    "julia": {
        "comment": "#",
        "suffix": "jl",
        "url": "https://github.com/tree-sitter/tree-sitter-julia",
    },
    "kotlin": {
        "comment": "//",
        "suffix": "kt",
        "url": "https://github.com/fwcd/tree-sitter-kotlin",
    },
    "lalrpop": {
        "comment": "//",
        "suffix": "lalrpop",
        "url": "https://github.com/traxys/tree-sitter-lalrpop",
    },
    "latex": {
        "comment": "%",
        "suffix": "tex",
        "url": "https://github.com/latex-lsp/tree-sitter-latex",
    },
    "lean": {
        "comment": "--",
        "suffix": "lean",
        "url": "https://github.com/Julian/tree-sitter-lean",
    },
    "llvm": {
        "comment": ";",
        "suffix": "ll",
        "url": "https://github.com/benwilliamgraham/tree-sitter-llvm",
    },
    "lua": {
        "comment": "--",
        "suffix": "lua",
        "url": "https://github.com/Azganoth/tree-sitter-lua",
    },
    "m68k": {
        "comment": ";",
        "suffix": "m68k",
        "url": "https://github.com/grahambates/tree-sitter-m68k",
    },
    "markdown": {
        "comment": "<!--",
        "suffix": "md",
        "url": "https://github.com/ikatyang/tree-sitter-markdown",
    },
    "matlab": {
        "comment": "%",
        "suffix": "m",
        "url": "https://github.com/acristoffers/tree-sitter-matlab",
    },
    "meson": {
        "comment": "#",
        "suffix": "meson",
        "url": "https://github.com/staysail/tree-sitter-meson",
    },
    "mumps": {"comment": ";", "suffix": "m", "url": None},
    "nix": {
        "comment": "#",
        "suffix": "nix",
        "url": "https://github.com/cstrahan/tree-sitter-nix",
    },
    "objc": {
        "comment": "//",
        "suffix": "m",
        "url": "https://github.com/jiyee/tree-sitter-objc",
    },
    "ocaml": {
        "comment": "(*",
        "suffix": "ml",
        "url": "https://github.com/tree-sitter/tree-sitter-ocaml",
    },
    "org": {
        "comment": "#",
        "suffix": "org",
        "url": "https://github.com/milisims/tree-sitter-org",
    },
    "pascal": {
        "comment": "//",
        "suffix": "pas",
        "url": "https://github.com/Isopod/tree-sitter-pascal",
    },
    "perl": {
        "comment": "#",
        "suffix": "pl",
        "url": "https://github.com/tree-sitter-perl/tree-sitter-perl",
    },
    "pgn": {
        "comment": "%",
        "suffix": "pgn",
        "url": "https://github.com/rolandwalker/tree-sitter-pgn",
    },
    "php": {
        "comment": "#",
        "suffix": "php",
        "url": "https://github.com/tree-sitter/tree-sitter-php",
    },
    "pod": {
        "comment": "=",
        "suffix": "pod",
        "url": "https://github.com/tree-sitter-perl/tree-sitter-pod",
    },
    "powershell": {
        "comment": "#",
        "suffix": "ps1",
        "url": "https://github.com/PowerShell/tree-sitter-PowerShell",
    },
    "proto": {
        "comment": "//",
        "suffix": "proto",
        "url": "https://github.com/mitchellh/tree-sitter-proto",
    },
    "python": {
        "comment": "#",
        "suffix": "py",
        "url": "https://github.com/tree-sitter/tree-sitter-python",
    },
    "qmljs": {
        "comment": "//",
        "suffix": "qml",
        "url": "https://github.com/yuja/tree-sitter-qmljs",
    },
    "r": {"comment": "#", "suffix": "r", "url": "https://github.com/r-lib/tree-sitter-r"},
    "racket": {
        "comment": ";;",
        "suffix": "rkt",
        "url": "https://github.com/6cdh/tree-sitter-racket",
    },
    "rasi": {
        "comment": "#",
        "suffix": "rasi",
        "url": "https://github.com/Fymyte/tree-sitter-rasi",
    },
    "re2c": {
        "comment": "//",
        "suffix": "re2c",
        "url": "https://github.com/alemuller/tree-sitter-re2c",
    },
    "regex": {
        "comment": "#",
        "suffix": "regex",
        "url": "https://github.com/tree-sitter/tree-sitter-regex",
    },
    "rego": {
        "comment": "#",
        "suffix": "rego",
        "url": "https://github.com/FallenAngel97/tree-sitter-rego",
    },
    "rst": {
        "comment": "..",
        "suffix": "rst",
        "url": "https://github.com/stsewd/tree-sitter-rst",
    },
    "ruby": {
        "comment": "#",
        "suffix": "rb",
        "url": "https://github.com/tree-sitter/tree-sitter-ruby",
    },
    "rust": {
        "comment": "//",
        "suffix": "rs",
        "url": "https://github.com/tree-sitter/tree-sitter-rust",
    },
    "scala": {
        "comment": "//",
        "suffix": "scala",
        "url": "https://github.com/tree-sitter/tree-sitter-scala",
    },
    "scheme": {
        "comment": ";;",
        "suffix": "scm",
        "url": "https://github.com/6cdh/tree-sitter-scheme",
    },
    "scss": {
        "comment": "//",
        "suffix": "scss",
        "url": "https://github.com/serenadeai/tree-sitter-scss",
    },
    "sexp": {
        "comment": ";",
        "suffix": "sexp",
        "url": "https://github.com/AbstractMachinesLab/tree-sitter-sexp",
    },
    "sfapex": {
        "comment": "//",
        "suffix": "cls",
        "url": "https://github.com/aheber/tree-sitter-sfapex",
    },
    "smali": {
        "comment": "#",
        "suffix": "smali",
        "url": "https://github.com/amaanq/tree-sitter-smali",
    },
    "sourcepawn": {
        "comment": "//",
        "suffix": "sp",
        "url": "https://github.com/nilshelmig/tree-sitter-sourcepawn",
    },
    "sparql": {
        "comment": "#",
        "suffix": "sparql",
        "url": "https://github.com/BonaBeavis/tree-sitter-sparql",
    },
    "sql": {
        "comment": "--",
        "suffix": "sql",
        "url": "https://github.com/m-novikov/tree-sitter-sql",
    },
    "sqlite": {
        "comment": "--",
        "suffix": "sqlite",
        "url": "https://github.com/dhcmrlchtdj/tree-sitter-sqlite",
    },
    "svelte": {
        "comment": "<!--",
        "suffix": "svelte",
        "url": "https://github.com/Himujjal/tree-sitter-svelte",
    },
    "swift": {
        "comment": "//",
        "suffix": "swift",
        "url": "https://github.com/alex-pinkus/tree-sitter-swift",
    },
    "systemrdl": {
        "comment": "//",
        "suffix": "systemrdl",
        "url": "https://github.com/SystemRDL/tree-sitter-systemrdl",
    },
    "template": {
        "comment": "<%#",
        "suffix": "txt",
        "url": "https://github.com/tree-sitter/tree-sitter-embedded-template",
    },
    "thrift": {
        "comment": "//",
        "suffix": "thrift",
        "url": "https://github.com/duskmoon314/tree-sitter-thrift",
    },
    "toml": {
        "comment": "#",
        "suffix": "toml",
        "url": "https://github.com/ikatyang/tree-sitter-toml",
    },
    "turtle": {
        "comment": "#",
        "suffix": "ttl",
        "url": "https://github.com/BonaBeavis/tree-sitter-turtle",
    },
    "twig": {
        "comment": "{#",
        "suffix": "twig",
        "url": "https://github.com/gbprod/tree-sitter-twig",
    },
    "typescript": {
        "comment": "//",
        "suffix": "ts",
        "url": "https://github.com/tree-sitter/tree-sitter-typescript",
    },
    "verilog": {
        "comment": "//",
        "suffix": "v",
        "url": "https://github.com/tree-sitter/tree-sitter-verilog",
    },
    "vhdl": {
        "comment": "--",
        "suffix": "vhdl",
        "url": "https://github.com/alemuller/tree-sitter-vhdl",
    },
    "vue": {
        "comment": "//",
        "suffix": "vue",
        "url": "https://github.com/ikatyang/tree-sitter-vue",
    },
    "wasm": {
        "comment": ";;",
        "suffix": "wasm",
        "url": "https://github.com/wasm-lsp/tree-sitter-wasm",
    },
    "wgsl": {
        "comment": "//",
        "suffix": "wgsl",
        "url": "https://github.com/mehmetoguzderin/tree-sitter-wgsl",
    },
    "yaml": {
        "comment": "#",
        "suffix": "yaml",
        "url": "https://github.com/ikatyang/tree-sitter-yaml",
    },
    "yang": {
        "comment": "//",
        "suffix": "yang",
        "url": "https://github.com/Hubro/tree-sitter-yang",
    },
    "zig": {
        "comment": ";",
        "suffix": "zig",
        "url": "https://github.com/maxxnino/tree-sitter-zig",
    },
}
