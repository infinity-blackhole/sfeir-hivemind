import argparse
import logging

import grpc

from sfeir.hivemind.protos import hivemind_pb2, hivemind_pb2_grpc


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=str, default="50051")
    return parser.parse_args()


def run(opts: argparse.Namespace):
    with grpc.insecure_channel(opts.host + ":" + opts.port) as channel:
        stub = hivemind_pb2_grpc.AgentStub(channel)
        response = stub.SayHello(hivemind_pb2.HelloRequest(name="you"))
        print("Agent client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run(parse_opt())
