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
                model: str = "gpt-3.5-turbo-1025",
                TOK_SIZES : list = [512, 1024, 2048, 4096, 8192, 16384, 100000, 200000],
                RESULT_DIRS : list = [
                                "ast-strict-results",
                                "file-results",
                                "tag-results",
                                "ast-flex-results-",
                                "chunk-results-",
                            ]
                ):
        self.model = model
        self.TOK_SIZES = TOK_SIZES
        self.RESULT_DIRS = RESULT_DIRS

    def run(self):
        kwargs = dict(
            model=self.model,
            source_language="mumps",
            max_prompts=10,
            max_tokens=1000000,
            comments_per_request=100,
        )

        # Documenters with fixed 1,000,000 token limit
        ast_strict_split = MadLibsDocumenter(custom_splitter="ast-strict", **kwargs)
        file_split = MadLibsDocumenter(custom_splitter="file", **kwargs)
        tag_split = MadLibsDocumenter(custom_splitter="tag", **kwargs)

        log.info("Running AST-STRICT splitting experiment.")
        ast_strict_split.translate(
            input_directory="llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input",
            output_directory="ast-strict-results",
        )
        log.info("AST-STRICT splitting experiment complete.")

        log.info("Running NO (FILE) splitting experiment.")
        file_split.translate(
            input_directory="llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input",
            output_directory="file-results",
        )
        log.info("NO (FILE) experiment complete")

        log.info("Running TAG splitting experiment.")
        tag_split.translate(
            input_directory="llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input",
            output_directory="tag-results",
        )
        log.info("TAG splitting experiment complete.")

        # Documenters that require varying token limits
        for TOKS in self.TOK_SIZES:
            kwargs["max_tokens"] = TOKS
            print(kwargs)
            ast_flex_split = MadLibsDocumenter(custom_splitter="ast-flex", **kwargs)
            chunk_split = MadLibsDocumenter(custom_splitter="chunk", **kwargs)

            log.info(f"Running AST-FLEX splitting experiment with {TOKS} as max token limit for model.")
            ast_flex_split.translate(
                input_directory="llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input",
                output_directory="ast-flex-results-" + str(TOKS),
            )
            log.info(f"AST-FLEX splitting experiment with {TOKS} as max token limit complete.")


            log.info(f"Running CHUNK splitting experiment with {TOKS} as max token limit for model.")
            chunk_split.translate(
                input_directory="llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input",
                output_directory="chunk-results-" + str(TOKS),
            )
            log.info(f"CHUNK splitting experiment with {TOKS} as max token limit complete.")

    def process_dirs(self):
        input_dir = Path(
            "llm-data/ITMod/documentation-tests/madlibs/mumps-incomplete-records-tracking/exhaustive-inline-comments-input/processed.json"
        ).expanduser()
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
        "--model",
        type=str,
        default="bedrock-llama3-70b-instruct",
        help="The LLM model to be used for comment generation"
    )

    parser.add_argument(
        "--max-token-sizes",
        nargs="+",
        type=int,
        default=[512, 1024, 2048, 4096, 8192, 16384, 100000, 200000]
    )

    # TODO: RESULTING DRS ARG... NECESSARY?
    args = parser.parse_args()
    experiment = Experimenter(args.model, args.max_token_sizes)
    experiment.run()
    experiment.process_dirs()
