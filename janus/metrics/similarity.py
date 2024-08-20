import click
import typer
from langchain.evaluation import EmbeddingDistance, load_evaluator
from typing_extensions import Annotated

from janus.embedding.embedding_models_info import load_embedding_model
from janus.metrics.metric import metric


@metric(name="similarity-score", help="Distance between embeddings of strings.")
def similarity_score(
    target: str,
    reference: str,
    model_name: Annotated[
        str,
        typer.Option("-e", "--embedding-model", help="Name of embedding model to use."),
    ] = "text-embedding-3-small",
    distance_metric: Annotated[
        str,
        typer.Option(
            "-d",
            "--distance-metric",
            click_type=click.Choice([e.value for e in list(EmbeddingDistance)]),
            help="Distance metric to use.",
        ),
    ] = "cosine",
    **kwargs,
) -> float:
    """Computes the similarity score of two strings

    Arguments:
        target: The target string.
        reference: The reference string.
        model_name: The name of the embedding model to use.
        distance_metric: The distance metric to use. Can be one of:
            - cosine
            - euclidean
            - manhattan
            - chebyshev
            - hamming

    Returns:
        The similarity score of the two strings.
    """
    embedding_model, _, _ = load_embedding_model(model_name)
    evaluator = load_evaluator(
        "pairwise_embedding_distance",
        embeddings=embedding_model,
        distance_metric=distance_metric,
    )
    return evaluator.evaluate_string_pairs(prediction=target, prediction_b=reference)[
        "score"
    ]
