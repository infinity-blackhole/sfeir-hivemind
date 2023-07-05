import bentoml
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

bentoml.pytorch.save_model("sentence-transformers", model)
