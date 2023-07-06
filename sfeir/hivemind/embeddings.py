import logging

import bentoml
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def run():
    bentoml.pytorch.save_model(
        "sfeir-hivemind-all-mpnet-base-v2",
        model,
        signatures={"encode": {"batchable": True, "batch_dim": 0}},
    )


if __name__ == "__main__":
    logging.basicConfig()
    run()
