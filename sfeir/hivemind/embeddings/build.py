import argparse
import logging

import bentoml
from sentence_transformers import SentenceTransformer


def run(opts: argparse.Namespace):
    model = SentenceTransformer(opts.model_id)

    bentoml.pytorch.save_model(
        "pt-sentence-transformers-all-mpnet-base-v2",
        model,
        signatures={"encode": {"batchable": True, "batch_dim": 0}},
    )


def parse_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-id", "-m", type=str, default="sentence-transformers/all-mpnet-base-v2"
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opts())
