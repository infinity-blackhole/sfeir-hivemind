import bentoml
from sentence_transformers import SentenceTransformer

bentoml.pytorch.save_model(
    "sfeir_hivemind_embeddings",
    SentenceTransformer("sentence-transformers/all-mpnet-base-v2"),
    signatures={"encode": {"batchable": True, "batch_dim": 0}},
)
