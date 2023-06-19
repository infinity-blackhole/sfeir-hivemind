import logging
import os
from concurrent import futures

import grpc

from sfeir.hivemind.protos import hivemind_pb2, hivemind_pb2_grpc


class Greeter(hivemind_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hivemind_pb2.HelloReply(message="Hello, %s!" % request.name)


def serve():
    host = os.environ.get("HOST", "[::]")
    port = os.environ.get("PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hivemind_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(host + ":" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
