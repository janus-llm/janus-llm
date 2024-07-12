import argparse
import json
from pathlib import Path
from scripts.combine_comment_jsons import parse_madlibs
from janus.utils.logger import create_logger
from janus.translate import MadLibsDocumenter

log = create_logger(__name__)

class Experimenter:

    """
    A class that conducts a series of comment generation experiments using different
    partitioning methods and token sizes for mumps code
    """
    def __init__(self,
                input_dir: str | None=None,
                source_language: str | None=None,
                model: str = "bedrock-llama3-70b-instruct",
                TOK_SIZES : list = [512, 1024, 2048, 4096, 8192, 16384, 100000, 200000],
                RESULT_DIRS : list = [
                                "ast-strict-results",
                                "file-results",
                                "tag-results",
                                "ast-flex-results-",
                                "chunk-results-",
                            ]
                ):
        self.input_dir = input_dir
        self.source_language = source_language
        self.model = model
        self.TOK_SIZES = TOK_SIZES
        self.RESULT_DIRS = RESULT_DIRS

    def run(self):
        kwargs = dict(
            model=self.model,
            source_language=self.source_language,
            max_prompts=10,
            max_tokens=1000000,
            comments_per_request=100,
        )

        # Documenters with fixed 1,000,000 token limit
        ast_strict_split = MadLibsDocumenter(custom_splitter="ast-strict", **kwargs)

        log.info("Running AST-STRICT splitting experiment.")
        ast_strict_split.translate(
            input_directory=self.input_dir,
            output_directory="ast-strict-results",
        )
        log.info("AST-STRICT splitting experiment complete.")

        # Only run FILE and TAG split if source language is mumps
        if self.source_language == "mumps":
            file_split = MadLibsDocumenter(custom_splitter="file", **kwargs)
            log.info("Running NO (FILE) splitting experiment.")
            file_split.translate(
                input_directory=self.input_dir,
                output_directory="file-results",
            )
            log.info("NO (FILE) splitting experiment complete")

            tag_split = MadLibsDocumenter(custom_splitter="tag", **kwargs)
            log.info("Running TAG splitting experiment.")
            tag_split.translate(
                input_directory=self.input_dir,
                output_directory="tag-results",
            )
            log.info("TAG splitting experiment complete.")

        # For running documenters that require varying token limits
        for TOKS in self.TOK_SIZES:
            kwargs["max_tokens"] = TOKS

            ast_flex_split = MadLibsDocumenter(custom_splitter="ast-flex", **kwargs)
            log.info(f"Running AST-FLEX splitting experiment with {TOKS} as max token limit for model.")
            ast_flex_split.translate(
                input_directory=self.input_dir,
                output_directory="ast-flex-results-" + str(TOKS),
            )
            log.info(f"AST-FLEX splitting experiment with {TOKS} as max token limit complete.")

            # Only run CHUNK split if source language is MUMPS
            if self.source_language == "mumps":
                chunk_split = MadLibsDocumenter(custom_splitter="chunk", **kwargs)
                log.info(f"Running CHUNK splitting experiment with {TOKS} as max token limit for model.")
                chunk_split.translate(
                    input_directory=self.input_dir,
                    output_directory="chunk-results-" + str(TOKS),
                )
                log.info(f"CHUNK splitting experiment with {TOKS} as max token limit complete.")

    def process_dirs(self):
        input_dir = Path(self.input_dir).expanduser()
        for DIR in self.RESULT_DIRS:
            if DIR.startswith("ast-flex", "chunk"):
                for TOK in self.TOK_SIZES:
                    log.info(f"Combining comment jsons for {DIR}")
                    output_dir = Path(DIR + str(TOK)).expanduser()
                    obj = parse_madlibs(input_dir, output_dir)
                    (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))
            else:
                log.info(f"Combining comment jsons for {DIR}")
                output_dir = Path(DIR).expanduser()
                obj = parse_madlibs(input_dir, output_dir)
                (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Mumps comment generation experiment",
        description=" conducts a series of comment generation experiments using different"
        "partitioning methods and token sizes for mumps code.",
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        # required=True, #! TESTING PURPOSE..RM CMT
        default="/Users/ppoudel/Documents/modern_eval/llm-data/ITMod/documentation-tests/madlibs/alc-walmart/comments-removed" #! TESTING PURPOSE..RM
    )

    parser.add_argument(
        "--source-language",
        tyoe=str,
        # required=True, #! TESTING PURPOSE RM CMT
        default='alc' #! TESTING PURPOSE RM 
    )

    parser.add_argument(
        "--model",
        type=str,
        default="bedrock-llama3-70b-instruct",
        help="The LLM model to be used for comment generation",
    )

    parser.add_argument(
        "--max-token-sizes",
        nargs="+",
        type=int,
        default=[512, 1024, 2048, 4096, 8192, 16384, 100000, 200000],
    )

    args = parser.parse_args()
    experiment = Experimenter(args.input_dir, args.source_language, args.model, args.max_token_sizes)
    experiment.run()
    experiment.process_dirs()
