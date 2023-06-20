import argparse
import logging

import bentoml
import docker

_logger = logging.getLogger(__name__)


def run(opts: argparse.Namespace):
    bento = bentoml.bentos.build(
        service="sfeir.hivemind.service:svc",
        include=["sfeir/hivemind/*.py"],
        docker={
            "python_version": "3.10",
        },
        python={
            "packages": [
                "deeplake<4,>=3.6.4",
                "google-api-core<3,>=2.11.1",
                "google-api-python-client<3,>=2.88",
                "google-auth-httplib2<1,>=0.1",
                "google-auth-oauthlib<2,>=1.0",
                "google-cloud-aiplatform<2.0,>=1.25.0",
                "google-cloud-core<3,>=2.3.2",
                "langchain[llms]<0.1,>=0.0.190",
                "pillow<10,>=9.5",
                "protobuf<4,>=3.20.3",
                "pydantic<2,>=1.10.9",
                "pypdf2<4,>=3.0",
                "sentence-transformers<3,>=2.2",
                "transformers<5,>=4.29",
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
    parser.add_argument("--tag", "-t", type=str, nargs="+", required=True)
    parser.add_argument("--push", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opts())
