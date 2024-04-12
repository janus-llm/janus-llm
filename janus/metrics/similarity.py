import click
import typer
from langchain.evaluation import EmbeddingDistance, load_evaluator
from typing_extensions import Annotated

from janus.embedding.embedding_models_info import load_embedding_model

from .metric import metric


@metric(name="similarity-score", help="Distance between embeddings of strings")
def similarity_score(
    targ: str,
    ref: str,
    model_name: Annotated[
        str,
        typer.Option("-em", "--embedding-model", help="Name of embedding model to use"),
    ] = "text-embedding-3-small",
    distance_metric: Annotated[
        str,
        typer.Option(
            "-dm",
            "--distance-metric",
            click_type=click.Choice([e.value for e in list(EmbeddingDistance)]),
            help="Distance metric to use",
        ),
    ] = "cosine",
    **kwargs,
) -> float:
    """
    Computes the similarity score of two strings
    :param targ target string to evaluate
    :param ref reference string
    :param model_name name of embedding model to use
    :param distance metric name of distance metric to use
    :param kwargs key word arguments

    """
    embedding_model, _, _ = load_embedding_model(model_name)
    evaluator = load_evaluator(
        "pairwise_embedding_distance",
        embeddings=embedding_model,
        distance_metric=distance_metric,
    )
    return evaluator.evaluate_string_pairs(prediction=targ, prediction_b=ref)["score"]
