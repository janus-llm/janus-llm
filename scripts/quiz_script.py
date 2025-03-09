from pathlib import Path

from janus.converter.translate import Translator
from janus.converter.requirements import RequirementsDocumenter
from janus.converter.quiz_generator import QuizGenerator
from janus.converter.quiz_taker import QuizTaker

import time

if __name__ == "__main__":
    print('running main function!')


    # quiz_gen = QuizGenerator(
    #     model="bedrock-mixtral",
    #     source_language="python",
    #     target_language="json",
    #     prompt_templates="quiz/quiz_generator"
    # )

    # quiz_gen.translate(
    #     input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff",
    #     output_directory="/home/faithmorgan/janus_dev/test_docs/quiz_gen_outputs",
    #     overwrite=True
    # )

    quiz_take = QuizTaker(
        model="bedrock-mixtral",
        source_language="python",
        target_language="json",
        prompt_templates="quiz/quiz_taker",
        use_janus_inputs=True
    )

    quiz_take.translate(
        input_directory="/home/faithmorgan/janus_dev/test_docs/quiz_gen_outputs",
        output_directory="/home/faithmorgan/janus_dev/test_docs/quiz_taker_outputs",
        overwrite=True
    )

    # chain = quiz_gen|quiz_take
    # chain.translate(
    #     input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff",
    #     output_directory="/home/faithmorgan/janus_dev/test_docs/end_output",
    #     overwrite=False
    # )


    # example_translator = Translator(
    #     model="bedrock-mixtral",
    #     source_language="python",
    #     target_language="json",
    #     prompt_templates="quiz_gen/translate_version"
    # )

    # example_translator.translate(
    #     input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff",
    #     output_directory="/home/faithmorgan/janus_dev/test_docs/c_stuff/",
    #     overwrite=True
    # )


    # example_quiz = RequirementsDocumenter(
    #     model="bedrock-mixtral",
    #     source_language="python",
    #     prompt_templates="requirements"
    # )

    # example_quiz.translate(
    #     input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff/",
    #     output_directory="/home/faithmorgan/janus_dev/test_docs/requirements_test/",
    #     overwrite=True
    # )




    