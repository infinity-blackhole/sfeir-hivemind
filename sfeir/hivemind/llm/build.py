import argparse
import logging

import openllm


def run(opts: argparse.Namespace):
    openllm.build(
        "llama",
        model_id=opts.model_id,
        quantize="int8",
    )


def parse_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opts())
