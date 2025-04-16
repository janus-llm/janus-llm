from janus.converter.quiz_generator import QuizGenerator
from janus.converter.quiz_taker import QuizTaker

if __name__ == "__main__":
    print("running main function!")

    # variables = [
    #     ("Algorithm", "Logic and flow of algorithms used in the code."),
    #     ("Data", "Types of data structures used and their roles."),
    #     ("Code", "Interpret and explain the purpose of specific code segments."),
    #     (
    #         "Design Patterns",
    #         """Pattern implementation, Architectural principles, Component interactions,
    #         Separation of concerns, Code organization principles.""",
    #     ),
    #     (
    #         "Language Features",
    #         "Understanding of language-specific constructs and idioms.",
    #     ),
    #     (
    #         "Error Handling",
    #         "Exception handling patterns, input validation, boundary conditions.",
    #     ),
    #     (
    #         "Function",
    #         """Know how to convert function signatures, parameters, and
    #         return types between languages.""",
    #     ),
    # ]
    variables = [
        ("algorithm", "Algorithm", "Logic and flow of algorithms used in the code."),
        ("data", "Data", "Types of data structures used and their roles."),
    ]

    for tag, topic, description in variables:
        for attempt in range(1, 6):  # Try up to 5 times
            try:
                quiz_gen = QuizGenerator(
                    # model="bedrock-mixtral",
                    model="bedrock-claude-sonnet",
                    source_language="python",
                    target_language="json",
                    prompt_templates="quiz/quiz_generator",
                    quiz_topic=topic,
                    quiz_topic_description=description,
                )

                quiz_gen.translate(
                    input_directory="temp_input_folder",
                    output_directory=f"janus-quiz/{tag}/",
                    overwrite=False,
                )

                quiz_take = QuizTaker(
                    # model="bedrock-mixtral",
                    model="bedrock-claude-sonnet",
                    source_language="python",
                    target_language="json",
                    prompt_templates="quiz/quiz_taker",
                    use_janus_inputs=True,
                )

                quiz_take.translate(
                    input_directory=f"janus-quiz/{tag}/",
                    output_directory=f"janus-quiz-results/{tag}/",
                    overwrite=False,
                )

                break  # Exit the loop if successful
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
