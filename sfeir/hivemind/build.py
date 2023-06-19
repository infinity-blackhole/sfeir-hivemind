import argparse

import bentoml


def parse_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", "-t", type=str, required=True)
    return parser.parse_args()


def run(opts: argparse.Namespace):
    bento = bentoml.bentos.build(
        service="sfeir.hivemind.service:svc",
        include=["sfeir/hivemind/service.py"],
        python={
            "packages": [
                "deeplake<4,>=3.6.4",
                "google-api-python-client<3,>=2.88",
                "google-auth-httplib2<1,>=0.1",
                "google-auth-oauthlib<2,>=1.0",
                "google-cloud-aiplatform<2.0,>=1.25.0",
                "langchain[llms]<0.1,>=0.0.190",
                "pillow<10,>=9.5",
                "pypdf2<4,>=3.0",
                "sentence-transformers<3,>=2.2",
                "transformers<5,>=4.29",
            ]
        },
        docker={
            "python_version": "3.10",
        },
    )

    bentoml.container.build(
        bento.tag, image_tag=tuple(opts.tag.split(":")), features=["grpc", "tracing"]
    )


if __name__ == "__main__":
    run(parse_opts())
