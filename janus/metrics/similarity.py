import click
import numpy as np
import typer
from langchain_classic.evaluation import EmbeddingDistance, load_evaluator
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
    try:
        result = evaluator.evaluate_string_pairs(
            prediction=target, prediction_b=reference
        )
        return float(result["score"])
    except AttributeError:
        # Workaround for langchain_classic bug where _compute_score calls .item()
        # on scipy distance results that return plain floats (e.g. euclidean)
        vec_a = np.array(embedding_model.embed_query(target))
        vec_b = np.array(embedding_model.embed_query(reference))
        metric_enum = EmbeddingDistance(distance_metric)
        if metric_enum == EmbeddingDistance.EUCLIDEAN:
            from scipy.spatial.distance import euclidean

            return float(euclidean(vec_a, vec_b))
        elif metric_enum == EmbeddingDistance.MANHATTAN:
            from scipy.spatial.distance import cityblock

            return float(cityblock(vec_a, vec_b))
        elif metric_enum == EmbeddingDistance.CHEBYSHEV:
            from scipy.spatial.distance import chebyshev

            return float(chebyshev(vec_a, vec_b))
        elif metric_enum == EmbeddingDistance.HAMMING:
            from scipy.spatial.distance import hamming

            return float(hamming(vec_a, vec_b))
        else:
            from sklearn.metrics.pairwise import cosine_distances

            return float(
                cosine_distances(vec_a.reshape(1, -1), vec_b.reshape(1, -1))[0][0]
            )
