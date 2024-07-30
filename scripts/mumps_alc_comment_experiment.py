import argparse
import json
from pathlib import Path

from janus.converter.document import MadLibsDocumenter
from janus.utils.logger import create_logger
from scripts.combine_comment_jsons import parse_madlibs

log = create_logger(__name__)


class Experimenter:

    """
    A class that conducts a series of comment generation experiments using different
    partitioning methods and token sizes for mumps or alc code.
    """

    def __init__(
        self,
        input_dir: str | None = None,
        output_dir: str | None = None,
        source_language: str | None = None,
        model: str = "gpt-3.5-turbo-0125",
        TOK_SIZES: list = [512, 1024, 2048, 4096, 8192, 16384, 100000, 200000],
        RESULT_DIRS: list = [
            "ast-strict",
            "file",
            "ast-flex",
            "chunk",
        ],
    ):
        """
        Initialize an Experimenter instance.

        Arguments:
            input_dir: Directory containing the input source code files.
            output_dir: Directory to store experiment results.
                NOTE: Ensure directory is language specific
                (e.g. data/mumps-irt-20240730/generated-comments)
            source_langauge: The language of the source code files.
                NOTE: If doing alc experiment, source langauge should be ibmhlasm
            model: The LLM to use for comment generation.
            TOK_SIZES: The varying tokens limits which certain splitting methods require.
                NOTE: Only the AST-FLEX and CHUNK splitting methods use varying token
                limits and that is hard coded into this script
            RESULT_DIRS: The names of the resulting output directories
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.source_language = source_language
        self.model = model
        self.TOK_SIZES = TOK_SIZES
        self.RESULT_DIRS = RESULT_DIRS

    def run(self):
        """
        Runs experiment and produces folders and output for each splitting experiment.
        """
        kwargs = dict(
            model=self.model,
            source_language=self.source_language,
            max_prompts=125,
            max_tokens=1000000,
            comments_per_request=10,
        )

        # Documenters with fixed 1,000,000 token limit
        file_split = MadLibsDocumenter(custom_splitter="file", **kwargs)
        log.info("Running FILE splitting experiment.")
        file_split.translate(
            input_directory=self.input_dir,
            output_directory=f"{self.output_dir}/{self.model}/file",
        )
        log.info("FILE splitting experiment complete")

        ast_strict_split = MadLibsDocumenter(custom_splitter="ast-strict", **kwargs)
        log.info("Running AST-STRICT splitting experiment.")
        ast_strict_split.translate(
            input_directory=self.input_dir,
            output_directory=f"{self.output_dir}/{self.model}/ast-strict",
        )
        log.info("AST-STRICT splitting experiment complete.")

        # For running documenters that require varying token limits
        for TOKS in self.TOK_SIZES:
            kwargs["max_tokens"] = TOKS

            chunk_split = MadLibsDocumenter(custom_splitter="chunk", **kwargs)
            log.info(
                f"Running CHUNK splitting experiment with {TOKS} "
                "as max token limit for model."
            )
            chunk_split.translate(
                input_directory=self.input_dir,
                output_directory=f"{self.output_dir}/{self.model}/chunk/{TOKS}",
            )
            log.info(
                f"CHUNK splitting experiment with {TOKS} as max token limit complete."
            )

            ast_flex_split = MadLibsDocumenter(custom_splitter="ast-flex", **kwargs)
            log.info(
                f"Running AST-FLEX splitting experiment with {TOKS} "
                "as max token limit for model."
            )
            ast_flex_split.translate(
                input_directory=self.input_dir,
                output_directory=f"{self.output_dir}/{self.model}/ast-flex/{TOKS}",
            )
            log.info(
                f"AST-FLEX splitting experiment with {TOKS} "
                "as max token limit complete."
            )

    def process_dirs(self):
        """
        Combine all of generated json outputs from experiment running into the
        processed.json format
        """
        input_file = Path(self.input_dir + "/processed.json").expanduser()
        for DIR in self.RESULT_DIRS:
            if "ast-flex" in DIR or "chunk" in DIR:
                for TOK in self.TOK_SIZES:
                    log.info(f"Combining comment jsons for {DIR}-{TOK}")
                    output_dir = Path(
                        f"{self.output_dir}/{self.model}/{DIR}/{TOK}"
                    ).expanduser()
                    obj = parse_madlibs(input_file, output_dir)
                    (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))
            else:
                log.info(f"Combining comment jsons for {DIR}")
                output_dir = Path(f"{self.output_dir}/{self.model}/{DIR}").expanduser()
                obj = parse_madlibs(input_file, output_dir)
                (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Mumps & ALC comment generation experiment",
        description="Conducts a series of comment generation experiments using different"
        "partitioning methods and token sizes for mumps and alc code.",
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory of source code files.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to store experiment results. Ensure directory is language "
        "specific (e.g. data/mumps-irt-20240730/generated-comments).",
    )

    parser.add_argument(
        "--source-language",
        type=str,
        required=True,
        help="If doing alc experiment, source langauge should be ibmhlasm, "
        "otherwise use mumps.",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo-0125",
        help="The LLM model to be used for comment generation",
    )

    parser.add_argument(
        "--max-token-sizes",
        nargs="+",
        type=int,
        default=[512, 1024, 2048, 4096, 8192, 16384, 100000, 200000],
        help="Specify the varying max tokens sizes for the ast-flex "
        "and chunk splitting method",
    )

    args = parser.parse_args()
    experiment = Experimenter(
        args.input_dir, args.source_language, args.model, args.max_token_sizes
    )
    experiment.run()
    experiment.process_dirs()
