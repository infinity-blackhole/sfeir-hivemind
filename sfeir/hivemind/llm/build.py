import openllm
import logging
import bentoml
import argparse
import docker

_logger = logging.getLogger(__name__)


def run(opts: argparse.Namespace):
    bento = openllm.build(
        "falcon",
        model_id=opts.model_id,
        quantize="int8",
        bettertransformer=True,
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
    parser.add_argument("--model-id", type=str, default="tiiuae/falcon-7b")
    parser.add_argument("--tag", "-t", type=str, nargs="+", required=True)
    parser.add_argument("--push", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opts())
