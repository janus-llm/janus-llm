from pathlib import Path

from janus.converter.translate import Translator
from janus.converter.quiz_generator import QuizGenerator
from janus.converter.quiz_taker import QuizTaker


if __name__ == "__main__":
    print('running main function!')

    # example_quiz = QuizGenerator(
    #     model="bedrock-mixtral",
    #     source_language="python",
    #     target_language="json",
    #     prompt_templates="quiz/quiz_generator"
    # )

    # example_quiz.translate(
    #     input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff",
    #     output_directory="/home/faithmorgan/janus_dev/test_docs/quiz_gen_outputs/",
    #     overwrite=True
    # )

    example_quiz = QuizTaker(
        model="bedrock-mixtral",
        source_language="json",
        target_language="json",
        prompt_templates="quiz/quiz_taker",
        use_janus_inputs=True
    )

    example_quiz.translate(
        input_directory="/home/faithmorgan/janus_dev/test_docs/quiz_gen_outputs",
        output_directory="/home/faithmorgan/janus_dev/test_docs/quiz_taker_outputs/",
        overwrite=True
    )


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




    