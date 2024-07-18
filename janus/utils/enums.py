from enum import Enum
from typing import Any, Dict, Set


class EmbeddingType(Enum):
    SOURCE = 1
    REQUIREMENT = 2
    SUMMARY = 3
    PSEUDO = 4
    TARGET = 5  # placeholder embeddings, are these useful for analysis?


CUSTOM_SPLITTERS: Set[str] = {"mumps", "binary", "ibmhlasm"}

LANGUAGES: Dict[str, Dict[str, Any]] = {
    "ada": {
        "comment": "--",
        "suffix": "adb",
        "url": "https://github.com/briot/tree-sitter-ada",
        "example": 'put_line("Hello, World!");\n',
    },
    "agda": {
        "comment": "--",
        "suffix": "agda",
        "url": "https://github.com/tree-sitter/tree-sitter-agda",
        "example": 'postulate HelloWorld : String;\nHelloWorld = "Hello, World!";\n',
    },
    "x86asm": {
        "comment": "//",
        "suffix": "s",
        "url": "https://github.com/bearcove/tree-sitter-x86asm",
        "example": "mov     rax, 60\nxor       rdi, rdi\n",
    },
    "bash": {
        "comment": "#",
        "suffix": "sh",
        "url": "https://github.com/tree-sitter/tree-sitter-bash",
        "example": 'echo "Hello world"\n',
    },
    "binary": {
        "comment": None,
        "suffix": "bin",
        "url": "https://github.com/tree-sitter/tree-sitter-c",
        "example": "04 00 00 00 cd 48 65 6c 6c 6f 2c 20 77 6f 72 6c 64",
    },
    "beancount": {
        "comment": ";",
        "suffix": "beancount",
        "url": "https://github.com/zwpaper/tree-sitter-beancount",
        "example": '2023-01-01 custom "Hello, World!"\n',
    },
    "bigquery": {
        "comment": "--",
        "suffix": "sql",
        "url": "https://github.com/takegue/tree-sitter-sql-bigquery",
        "example": 'SELECT "Hello, World!" AS message;\n',
    },
    "c": {
        "comment": "//",
        "suffix": "c",
        "url": "https://github.com/tree-sitter/tree-sitter-c",
        "example": (
            '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n'
            "    return 0;\n}\n"
        ),
        "functional_node_types": ["function_definition"],
        "comment_node_type": "comment",
    },
    "capnp": {
        "comment": "#",
        "suffix": "capnp",
        "url": "https://github.com/amaanq/tree-sitter-capnp",
        "example": (
            "using Capnp;\n\nstruct HelloWorld @0x1234 {\n  greeting @0 :Text;\n}\n"
        ),
    },
    "cmake": {
        "comment": "#",
        "suffix": "cmake",
        "url": "https://github.com/uyha/tree-sitter-cmake",
        "example": (
            "cmake_minimum_required(VERSION 3.0)\nproject(HelloWorld)\n\n"
            'message("Hello, World!")\n'
        ),
    },
    "comment": {
        "comment": "#",
        "suffix": "comment",
        "url": "https://github.com/stsewd/tree-sitter-comment",
        "example": "# This is a comment\n",
    },
    "commonlisp": {
        "comment": ";;",
        "suffix": "lisp",
        "url": "https://github.com/theHamsta/tree-sitter-commonlisp",
        "example": '(format t "Hello, World!~%")\n',
    },
    "config": {
        "comment": "#",
        "suffix": None,
        "url": "https://github.com/metio/tree-sitter-ssh-client-config",
        "example": (
            "# Configuration for SSH Client\nHost my_server\n"
            "  HostName example.com\n  User my_username\n"
        ),
    },
    "css": {
        "comment": "/*",
        "suffix": "css",
        "url": "https://github.com/tree-sitter/tree-sitter-css",
        "example": 'body {\n    content: "Hello, World!";\n}\n',
    },
    "cuda": {
        "comment": "//",
        "suffix": "cu",
        "url": "https://github.com/theHamsta/tree-sitter-cuda",
        "example": (
            '#include <iostream>\n\n__global__ void hello() {\n    printf("Hello, '
            'World!\\n");\n}\n\nint main() {\n    hello<<<1, 1>>>();\n    '
            "cudaDeviceSynchronize();\n    return 0;\n}\n"
        ),
    },
    "d": {
        "comment": "//",
        "suffix": "d",
        "url": "https://github.com/gdamore/tree-sitter-d",
        "example": (
            'import std.stdio;\n\nvoid main() {\n    writeln("Hello, World!");\n}\n'
        ),
    },
    "dart": {
        "comment": "//",
        "suffix": "dart",
        "url": "https://github.com/UserNobody14/tree-sitter-dart",
        "example": "void main() {\n  print('Hello, World!');\n}\n",
    },
    "dockerfile": {
        "comment": "#",
        "suffix": "Dockerfile",
        "url": "https://github.com/camdencheek/tree-sitter-dockerfile",
        "example": "FROM ubuntu\n\nRUN echo 'Hello, World!'\n",
    },
    "dot": {
        "comment": "//",
        "suffix": "dot",
        "url": "https://github.com/rydesun/tree-sitter-dot",
        "example": 'graph HelloWorld {\n  label="Hello, World!"\n}\n',
    },
    "elisp": {
        "comment": ";;",
        "suffix": "el",
        "url": "https://github.com/Wilfred/tree-sitter-elisp",
        "example": '(message "Hello, World!")\n',
    },
    "elixir": {
        "comment": "#",
        "suffix": "ex",
        "url": "https://github.com/elixir-lang/tree-sitter-elixir",
        "example": 'IO.puts "Hello, World!"\n',
    },
    "elm": {
        "comment": "--",
        "suffix": "elm",
        "url": "https://github.com/elm-tooling/tree-sitter-elm",
        "example": (
            'import Browser\n\nmain = Browser.sandbox { init = "Hello, World!" }\n'
        ),
    },
    "eno": {
        "comment": "#",
        "suffix": "eno",
        "url": "https://github.com/eno-lang/tree-sitter-eno",
        "example": "message: Hello, World!\n",
    },
    "erlang": {
        "comment": "%",
        "suffix": "erl",
        "url": "https://github.com/WhatsApp/tree-sitter-erlang",
        "example": (
            "-module(hello).\n-export([world/0]).\n\nworld() ->\n"
            '    io:format("Hello, World!~n").\n'
        ),
    },
    "fennel": {
        "comment": ";",
        "suffix": "fnl",
        "url": "https://github.com/travonted/tree-sitter-fennel",
        "example": '(print "Hello, World!")\n',
    },
    "fish": {
        "comment": "#",
        "suffix": "fish",
        "url": "https://github.com/ram02z/tree-sitter-fish",
        "example": 'echo "Hello, World!"\n',
    },
    "formula": {
        "comment": ";",
        "suffix": "formula",
        "url": "https://github.com/siraben/tree-sitter-formula",
        "example": "A1: Hello, World!\n",
    },
    "fortran": {
        "comment": "!",
        "suffix": "f90",
        "url": "https://github.com/stadelmanma/tree-sitter-fortran",
        "example": (
            "program HelloWorld\n  print *, 'Hello, World!'\nend program HelloWorld\n"
        ),
        "functional_node_types": ["function"],
        "comment_node_type": "comment",
    },
    "gitattributes": {
        "comment": "#",
        "suffix": "gitattributes",
        "url": "https://github.com/ObserverOfTime/tree-sitter-gitattributes",
        "example": "* text=auto\n",
    },
    "gitignore": {
        "comment": "#",
        "suffix": "gitignore",
        "url": "https://github.com/shunsambongi/tree-sitter-gitignore",
        "example": "*.log\n",
    },
    "gleam": {
        "comment": "//",
        "suffix": "gleam",
        "url": "https://github.com/gleam-lang/tree-sitter-gleam",
        "example": 'pub fn main() {\n    io.print("Hello, World!")\n}\n',
    },
    "glsl": {
        "comment": "//",
        "suffix": "glsl",
        "url": "https://github.com/theHamsta/tree-sitter-glsl",
        "example": "void main() {\n    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n}\n",
    },
    "go": {
        "comment": "//",
        "suffix": "go",
        "url": "https://github.com/tree-sitter/tree-sitter-go",
        "example": (
            'package main\n\nimport "fmt"\n\nfunc main() {\n'
            '    fmt.Println("Hello, World!")\n}\n'
        ),
    },
    "graphql": {
        "comment": "#",
        "suffix": "graphql",
        "url": "https://github.com/bkegley/tree-sitter-graphql",
        "example": "query {\n  hello\n}\n",
    },
    "hack": {
        "comment": "//",
        "suffix": "hack",
        "url": "https://github.com/slackhq/tree-sitter-hack",
        "example": '<?hh\n\necho "Hello, World!";\n',
    },
    "haskell": {
        "comment": "--",
        "suffix": "hs",
        "url": "https://github.com/tree-sitter/tree-sitter-haskell",
        "example": 'main :: IO ()\nmain = putStrLn "Hello, World!"\n',
    },
    "hcl": {
        "comment": "#",
        "suffix": "hcl",
        "url": "https://github.com/MichaHoffmann/tree-sitter-hcl",
        "example": 'variable "message" {\n  default = "Hello, World!"\n}\n',
    },
    "html": {
        "comment": "<!--",
        "suffix": "html",
        "url": "https://github.com/tree-sitter/tree-sitter-html",
        "example": (
            "<html>\n<head>\n  <title>Hello, World!</title>\n</head>\n<body>\n  <h1>Hello"
            ", World!</h1>\n</body>\n</html>\n"
        ),
    },
    "ibmhlasm": {
        "comment": "*",
        "suffix": "asm",
        "url": "https://github.com/janus-llm/tree-sitter-ibmhlasm.git",
        "branch": "metrics",
        "example": (
            """
                     TITLE 'Hello, World! Program'
            HELLO    CSECT
                     STM   14,12,12(13)
                     LR    12,15
                     USING *,12
                     LA    15,SAVEAREA
                     ST    13,4(,15)
                     ST    15,8(13)
                     LR    13,15
                     WTO   'Hello, World!'
                     L     13,4(,13)
                     LM    14,12,12(13)
                     LA    15,0
                     BR    14
            SAVEAREA DS    18F
                     END   HELLO
        """
        ),
        "functional_node_types": ["csect", "dsect"],
        "branch_node_types": ["branch_instruction"],
        "operation_node_types": ["operation", "branch_operation"],
        "operand_node_types": ["operands"],
    },
    "java": {
        "comment": "//",
        "suffix": "java",
        "url": "https://github.com/tree-sitter/tree-sitter-java",
        "example": (
            "public class HelloWorld {\n    public static void main(String[] args) {\n"
            '        System.out.println("Hello, World!");\n    }\n}\n'
        ),
    },
    "javascript": {
        "comment": "//",
        "suffix": "js",
        "url": "https://github.com/tree-sitter/tree-sitter-javascript",
        "example": "console.log('Hello, World!');\n",
    },
    "jq": {
        "comment": "#",
        "suffix": "jq",
        "url": "https://github.com/flurie/tree-sitter-jq",
        "example": ".\n",
    },
    "json": {
        "comment": "//",
        "suffix": "json",
        "url": "https://github.com/tree-sitter/tree-sitter-json",
        "example": '{\n  "message": "Hello, World!"\n}\n',
    },
    "json5": {
        "comment": "//",
        "suffix": "json5",
        "url": "https://github.com/Joakker/tree-sitter-json5",
        "example": "{\n  message: 'Hello, World!'\n}\n",
    },
    "julia": {
        "comment": "#",
        "suffix": "jl",
        "url": "https://github.com/tree-sitter/tree-sitter-julia",
        "example": 'println("Hello, World!")\n',
    },
    "kotlin": {
        "comment": "//",
        "suffix": "kt",
        "url": "https://github.com/fwcd/tree-sitter-kotlin",
        "example": 'fun main() {\n    println("Hello, World!")\n}\n',
    },
    "lalrpop": {
        "comment": "//",
        "suffix": "lalrpop",
        "url": "https://github.com/traxys/tree-sitter-lalrpop",
        "example": (
            "grammar Hello {\n    extern {\n        fn print(s: &str);\n    }\n\n"
            "    pub token Integer = r'\\d+';\n    pub rule hello() = \"Hello, \" "
            "Integer;\n}\n"
        ),
    },
    "latex": {
        "comment": "%",
        "suffix": "tex",
        "url": "https://github.com/latex-lsp/tree-sitter-latex",
        "example": (
            "\\documentclass{article}\n\\begin{document}\n  Hello, "
            "World!\n\\end{document}\n"
        ),
    },
    "lean": {
        "comment": "--",
        "suffix": "lean",
        "url": "https://github.com/Julian/tree-sitter-lean",
        "example": 'def main : io io.unit := io.put_str_ln "Hello, World!"\n',
    },
    "llvm": {
        "comment": ";",
        "suffix": "ll",
        "url": "https://github.com/benwilliamgraham/tree-sitter-llvm",
        "example": (
            "; ModuleID = 'hello.ll'\n\ndefine void @main() {\nentry:\n  call void "
            "@puts(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i32 0, "
            "i32 0))\n  ret void\n}\n\n@.str = private unnamed_addr constant [14 x i8] "
            'c"Hello, World!\\0A\\00", align 1\n'
        ),
    },
    "lua": {
        "comment": "--",
        "suffix": "lua",
        "url": "https://github.com/Azganoth/tree-sitter-lua",
        "example": 'print("Hello, World!")\n',
    },
    "m68k": {
        "comment": ";",
        "suffix": "m68k",
        "url": "https://github.com/grahambates/tree-sitter-m68k",
        "example": "moveq #0,d0\n",
    },
    "markdown": {
        "comment": "<!--",
        "suffix": "md",
        "url": "https://github.com/ikatyang/tree-sitter-markdown",
        "example": "# Hello, World!\n\nThis is a Markdown document.\n",
    },
    "matlab": {
        "comment": "%",
        "suffix": "m",
        "url": "https://github.com/acristoffers/tree-sitter-matlab",
        "example": "fprintf('Hello, World!\\n');\n",
    },
    "meson": {
        "comment": "#",
        "suffix": "meson",
        "url": "https://github.com/staysail/tree-sitter-meson",
        "example": "project('hello', 'c')\n\nexecutable('hello', 'hello.c')\n",
    },
    "mumps": {
        "comment": ";",
        "suffix": "m",
        "url": "https://github.com/janus-llm/tree-sitter-mumps",
        "example": 'WRITE "Hello, World!"',
        "functional_node_types": ["routine_definition"],
        "comment_node_type": "comment",
        "branch_node_types": ["if_statement"],
        "operation_node_types": [
            "command",
            "function_call",
            "routine_call",
            "routine_definition",
        ],
        "operand_node_types": ["argument"],
    },
    "nix": {
        "comment": "#",
        "suffix": "nix",
        "url": "https://github.com/cstrahan/tree-sitter-nix",
        "example": '{ message = "Hello, World!"; }\n',
    },
    "objc": {
        "comment": "//",
        "suffix": "m",
        "url": "https://github.com/jiyee/tree-sitter-objc",
        "example": (
            "#import <Foundation/Foundation.h>\n\nint main() {\n    "
            '@autoreleasepool {\n        NSLog(@"Hello, World!");\n    }\n'
            "    return 0;\n}\n"
        ),
    },
    "ocaml": {
        "comment": "(*",
        "suffix": "ml",
        "url": "https://github.com/tree-sitter/tree-sitter-ocaml",
        "example": 'print_endline "Hello, World!";;\n',
    },
    "org": {
        "comment": "#",
        "suffix": "org",
        "url": "https://github.com/milisims/tree-sitter-org",
        "example": "#+TITLE: Hello, World!\n\nThis is an Org mode document.\n",
    },
    "pascal": {
        "comment": "//",
        "suffix": "pas",
        "url": "https://github.com/Isopod/tree-sitter-pascal",
        "example": "// Hello, World!\nWRITE 'Hello, World!'\n",
    },
    "perl": {
        "comment": "#",
        "suffix": "pl",
        "url": "https://github.com/tree-sitter-perl/tree-sitter-perl",
        "example": "# Hello, World!\nprint 'Hello, World!\\n';\n",
    },
    "pgn": {
        "comment": "%",
        "suffix": "pgn",
        "url": "https://github.com/rolandwalker/tree-sitter-pgn",
        "example": '% Hello, World!\nWRITE "Hello, World!"\n',
    },
    "php": {
        "comment": "#",
        "suffix": "php",
        "url": "https://github.com/tree-sitter/tree-sitter-php",
        "example": "<?php\n// Hello, World!\necho 'Hello, World!';\n",
    },
    "pod": {
        "comment": "=",
        "suffix": "pod",
        "url": "https://github.com/tree-sitter-perl/tree-sitter-pod",
        "example": "=head1 Hello, World!\n\nHello, World!\n\n=cut\n",
    },
    "powershell": {
        "comment": "#",
        "suffix": "ps1",
        "url": "https://github.com/PowerShell/tree-sitter-PowerShell",
        "example": "# Hello, World!\nWrite-Host 'Hello, World!'\n",
    },
    "proto": {
        "comment": "//",
        "suffix": "proto",
        "url": "https://github.com/mitchellh/tree-sitter-proto",
        "example": "// Hello, World!\nmessage HelloWorld {\n  string message = 1;\n}\n",
    },
    "pseudocode": {
        "comment": "",
        "suffix": "txt",
        "url": "",
        "example": "print Hello, World!",
    },
    "python": {
        "comment": "#",
        "suffix": "py",
        "url": "https://github.com/tree-sitter/tree-sitter-python",
        "example": "# Hello, World!\nprint('Hello, World!')\n",
        "functional_node_types": ["function_definition"],
        "comment_node_type": "comment",
    },
    "qmljs": {
        "comment": "//",
        "suffix": "qml",
        "url": "https://github.com/yuja/tree-sitter-qmljs",
        "example": (
            "// Hello, World!\nimport QtQuick 2.0\n\nItem {\n  Text { text: "
            "'Hello, World!' }\n}\n"
        ),
    },
    "r": {
        "comment": "#",
        "suffix": "r",
        "url": "https://github.com/r-lib/tree-sitter-r",
        "example": "# Hello, World!\nprint('Hello, World!')\n",
    },
    "racket": {
        "comment": ";;",
        "suffix": "rkt",
        "url": "https://github.com/6cdh/tree-sitter-racket",
        "example": ';; Hello, World!\n(displayln "Hello, World!")\n',
    },
    "rasi": {
        "comment": "#",
        "suffix": "rasi",
        "url": "https://github.com/Fymyte/tree-sitter-rasi",
        "example": "# Hello, World!\nprint('Hello, World!')\n",
    },
    "re2c": {
        "comment": "//",
        "suffix": "re2c",
        "url": "https://github.com/alemuller/tree-sitter-re2c",
        "example": '// Hello, World!\n{printf("Hello, World!\\n");}',
    },
    "regex": {
        "comment": "#",
        "suffix": "regex",
        "url": "https://github.com/tree-sitter/tree-sitter-regex",
        "example": "# Hello, World!\n# Match 'Hello, World!' with a regex\n",
    },
    "rego": {
        "comment": "#",
        "suffix": "rego",
        "url": "https://github.com/FallenAngel97/tree-sitter-rego",
        "example": '# Hello, World!\npackage hello\n\nmain = {\n  "Hello, World!"\n}\n',
    },
    "rst": {
        "comment": "..",
        "suffix": "rst",
        "url": "https://github.com/stsewd/tree-sitter-rst",
        "example": ".. Hello, World!\n\nHello, World!\n",
    },
    "ruby": {
        "comment": "#",
        "suffix": "rb",
        "url": "https://github.com/tree-sitter/tree-sitter-ruby",
        "example": "# Hello, World!\nputs 'Hello, World!'\n",
    },
    "rust": {
        "comment": "//",
        "suffix": "rs",
        "url": "https://github.com/tree-sitter/tree-sitter-rust",
        "example": '// Hello, World!\nfn main() {\n    println!("Hello, World!");\n}\n',
    },
    "scala": {
        "comment": "//",
        "suffix": "scala",
        "url": "https://github.com/tree-sitter/tree-sitter-scala",
        "example": (
            "// Hello, World!\nobject HelloWorld {\n  def main(args: "
            'Array[String]): Unit = {\n    println("Hello, World!")\n  }\n}\n'
        ),
    },
    "scheme": {
        "comment": ";;",
        "suffix": "scm",
        "url": "https://github.com/6cdh/tree-sitter-scheme",
        "example": ';; Hello, World!\n(displayln "Hello, World!")\n',
    },
    "scss": {
        "comment": "//",
        "suffix": "scss",
        "url": "https://github.com/serenadeai/tree-sitter-scss",
        "example": "// Hello, World!\n$variable: 'Hello, World!';\n",
    },
    "sexp": {
        "comment": ";",
        "suffix": "sexp",
        "url": "https://github.com/AbstractMachinesLab/tree-sitter-sexp",
        "example": '; Hello, World!\n(println "Hello, World!")\n',
    },
    "sfapex": {
        "comment": "//",
        "suffix": "cls",
        "url": "https://github.com/aheber/tree-sitter-sfapex",
        "example": (
            "// Hello, World!\npublic class HelloWorld {\n    public static void "
            'main(String[] args) {\n        System.out.println("Hello, World!");\n    '
            "}\n}\n"
        ),
    },
    "smali": {
        "comment": "#",
        "suffix": "smali",
        "url": "https://github.com/amaanq/tree-sitter-smali",
        "example": (
            ".class public LHelloWorld;\n.super Ljava/lang/Object;\n\n.method "
            "public static main([Ljava/lang/String;)V\n    .registers 2\n\n    "
            "sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;\n    "
            'const-string v1, "Hello, World!"\n    invoke-virtual {v0, v1}, '
            "Ljava/io/PrintStream;->println(Ljava/lang/String;)V\n\n    "
            "return-void\n.end method\n"
        ),
    },
    "sourcepawn": {
        "comment": "//",
        "suffix": "sp",
        "url": "https://github.com/nilshelmig/tree-sitter-sourcepawn",
        "example": (
            "#include <sourcemod>\n\npublic Plugin:myinfo = \n{\n    name    = "
            '"Hello World",\n    author  = "You",\n    version = "1.0",\n    url     = '
            '"",\n    description = "",\n};\n\nvoid OnPluginStart()\n{\n    '
            'PrintToServer("Hello, World!");\n}\n'
        ),
    },
    "sparql": {
        "comment": "#",
        "suffix": "sparql",
        "url": "https://github.com/BonaBeavis/tree-sitter-sparql",
        "example": 'SELECT "Hello, World!"',
    },
    "sql": {
        "comment": "--",
        "suffix": "sql",
        "url": "https://github.com/m-novikov/tree-sitter-sql",
        "example": "SELECT 'Hello, World!';",
    },
    "sqlite": {
        "comment": "--",
        "suffix": "sqlite",
        "url": "https://github.com/dhcmrlchtdj/tree-sitter-sqlite",
        "example": "SELECT 'Hello, World!';",
    },
    "svelte": {
        "comment": "<!--",
        "suffix": "svelte",
        "url": "https://github.com/Himujjal/tree-sitter-svelte",
        "example": "<script>\n  console.log('Hello, World!');\n</script>\n",
    },
    "swift": {
        "comment": "//",
        "suffix": "swift",
        "url": "https://github.com/alex-pinkus/tree-sitter-swift",
        "example": 'print("Hello, World!")\n',
    },
    "systemrdl": {
        "comment": "//",
        "suffix": "systemrdl",
        "url": "https://github.com/SystemRDL/tree-sitter-systemrdl",
        "example": (
            "address_space {\n  reg my_register {\n    address 0x0;\n    "
            "field my_field {\n      bits 0;\n      access r; // Read-only\n"
            "      reset 0;\n      hardware_bug; // It's a feature!\n    }\n  }\n}\n"
        ),
    },
    "template": {
        "comment": "<%#",
        "suffix": "txt",
        "url": "https://github.com/tree-sitter/tree-sitter-embedded-template",
        "example": "<%# Hello, World! %>\nHello, World!\n",
    },
    "text": {
        "comment": "",
        "suffix": "txt",
        "url": None,
        "example": "Hello, World!",
    },
    "thrift": {
        "comment": "//",
        "suffix": "thrift",
        "url": "https://github.com/duskmoon314/tree-sitter-thrift",
        "example": (
            "namespace py tutorial\n\nconst string HELLO_URL = "
            '"http://example.com/hello"\n\nstruct HelloRequest {}\n\nstruct '
            "HelloResponse {}\n\nservice HelloWorld {\n  HelloResponse hello(1: "
            "HelloRequest request)\n}\n"
        ),
    },
    "toml": {
        "comment": "#",
        "suffix": "toml",
        "url": "https://github.com/ikatyang/tree-sitter-toml",
        "example": 'message = "Hello, World!"\n',
    },
    "turtle": {
        "comment": "#",
        "suffix": "ttl",
        "url": "https://github.com/BonaBeavis/tree-sitter-turtle",
        "example": (
            "@prefix ex: <http://example.org/> .\n\nex:hello ex:message "
            '"Hello, World!" .\n'
        ),
    },
    "twig": {
        "comment": "{#",
        "suffix": "twig",
        "url": "https://github.com/gbprod/tree-sitter-twig",
        "example": "{# Hello, World! #}\nHello, World!\n",
    },
    "typescript": {
        "comment": "//",
        "suffix": "ts",
        "url": "https://github.com/tree-sitter/tree-sitter-typescript",
        "example": "console.log('Hello, World!');\n",
    },
    "uml": {
        "comment": "'",
        "suffix": "uml",
        "url": "https://github.com/lyndsysimon/tree-sitter-plantuml",
        "example": "@startuml\nAlice -> Bob: Authentication Request\nBob --> Alice:\
              Authentication Response\nAlice -> Bob: Another authentication\
              Request\nAlice <-- Bob: Another authentication Response\n@enduml",
    },
    "verilog": {
        "comment": "//",
        "suffix": "v",
        "url": "https://github.com/tree-sitter/tree-sitter-verilog",
        "example": (
            "module HelloWorld;\n  initial begin\n    "
            '$display("Hello, World!");\n  end\nendmodule\n'
        ),
    },
    "vhdl": {
        "comment": "--",
        "suffix": "vhdl",
        "url": "https://github.com/alemuller/tree-sitter-vhdl",
        "example": (
            "library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n\nentity "
            "HelloWorld is\nend HelloWorld;\n\narchitecture Behavioral of HelloWorld is"
            '\nbegin\n  process\n  begin\n    report "Hello, World!";\n    wait;\n  end '
            "process;\nend Behavioral;\n"
        ),
    },
    "vue": {
        "comment": "//",
        "suffix": "vue",
        "url": "https://github.com/ikatyang/tree-sitter-vue",
        "example": "<template>\n  <div>\n    Hello, World!\n  </div>\n</template>\n",
    },
    "wasm": {
        "comment": ";;",
        "suffix": "wasm",
        "url": "https://github.com/wasm-lsp/tree-sitter-wasm",
        "example": (
            '(module\n  (func $main (export "main")\n    (import "env" "puts" '
            "(func $puts (param i32)))\n    (call $puts (i32.const 0))\n  )\n)"
        ),
    },
    "wgsl": {
        "comment": "//",
        "suffix": "wgsl",
        "url": "https://github.com/mehmetoguzderin/tree-sitter-wgsl",
        "example": (
            "[[stage(fragment)]]\nfn main() -> [[builtin(position)]] "
            "vec4<f32> {\n    return vec4<f32>(1.0, 0.0, 0.0, 1.0);\n}\n"
        ),
    },
    "yaml": {
        "comment": "#",
        "suffix": "yaml",
        "url": "https://github.com/ikatyang/tree-sitter-yaml",
        "example": "message: Hello, World!\n",
    },
    "yang": {
        "comment": "//",
        "suffix": "yang",
        "url": "https://github.com/Hubro/tree-sitter-yang",
        "example": (
            "module hello-world {\n  yang-version 1.1;\n  namespace "
            '"urn:example:hello-world";\n\n  prefix hw;\n\n  container hello-world {\n'
            '    leaf message {\n      type string;\n      default "Hello, World!";\n'
            "    }\n  }\n}\n"
        ),
    },
    "zig": {
        "comment": ";",
        "suffix": "zig",
        "url": "https://github.com/maxxnino/tree-sitter-zig",
        "example": (
            'const std = @import("std");\n\npub fn main() void {\n    const '
            'stdout = std.io.getStdOut();\n    stdout.print("Hello, World!\\n");\n}\n'
        ),
    },
}
