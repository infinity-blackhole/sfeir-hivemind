import bentoml
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

bentoml.pytorch.save_model(
    "sfeir-hivemind-all-mpnet-base-v2",
    model,
    signatures={"encode": {"batchable": True, "batch_dim": 0}},
)
