import argparse
import logging

import bentoml
import docker

from sfeir.hivemind.embeddings import service


from sentence_transformers import SentenceTransformer

_logger = logging.getLogger(__name__)


def run(opts: argparse.Namespace):
    model = SentenceTransformer(opts.model_id)

    bentoml.pytorch.save_model(
        "sentence-transformers-all-mpnet-base-v2",
        model,
        signatures={"encode": {"batchable": True, "batch_dim": 0}},
    )

    bento = bentoml.bentos.build(
        service=f"{service.__name__}:svc",
        include=["sfeir/hivemind/*.py"],
        docker={
            "python_version": "3.10",
        },
        python={
            "packages": [
                "sentence-transformers<3,>=2.2",
                "torch<3,>=2.0.1",
            ]
        },
    )

    _logger.info(f"Built BentoML service {bento.tag}")

    bentoml.container.build(
        bento.tag, image_tag=tuple(opts.tag), features=["grpc", "tracing"]
    )

    _logger.info(f"Built Docker image {opts.tag} for BentoML service {bento.tag}")

    if opts.push:
        docker_client = docker.from_env()
        for tag in opts.tag:
            docker_client.images.push(tag)
            _logger.info(f"Pushed Docker image {opts.tag}")
    else:
        _logger.info(f"Skipping Docker image push for {opts.tag}")


def parse_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-id", "-m", type=str, default="sentence-transformers/all-mpnet-base-v2"
    )
    parser.add_argument("--tag", "-t", type=str, nargs="+", required=True)
    parser.add_argument("--push", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opts())
