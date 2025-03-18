from pathlib import Path

from janus.converter.quiz_generator import QuizGenerator
from janus.converter.quiz_taker import QuizTaker

if __name__ == "__main__":
    print('running main function!')


    quiz_gen = QuizGenerator(
        # model="bedrock-mixtral",
        model="bedrock-claude-sonnet",
        source_language="python",
        target_language="json",
        prompt_templates="quiz/quiz_generator"
    )

    quiz_gen.translate(
        input_directory="/home/faithmorgan/janus_dev/test_docs/python_stuff",
        output_directory="/home/faithmorgan/janus_dev/test_docs/quiz_gen_outputs",
        overwrite=True
    )

    quiz_take = QuizTaker(
        # model="bedrock-mixtral",
        model="bedrock-claude-sonnet",
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

    