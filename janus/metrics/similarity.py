from langchain.evaluation import load_evaluator

from janus.embedding.embedding_models_info import load_embedding_model

from .metric import metric


@metric()
def similarity_score(targ: str, ref: str, **kwargs):
    embedding_model, _, _ = load_embedding_model("text-embedding-3-small")
    evaluator = load_evaluator("pairwise_embedding_distance", embeddings=embedding_model)
    return evaluator.evaluate_string_pairs(prediction=targ, prediction_b=ref)["score"]
