import bentoml
import openllm
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

bentoml.pytorch.save_model(
    "sentence-transformers",
    model,
    signatures={"encode": {"batchable": True, "batch_dim": 0}},
)

openllm.build("stablelm", model_id="stabilityai/stablelm-tuned-alpha-3b")
