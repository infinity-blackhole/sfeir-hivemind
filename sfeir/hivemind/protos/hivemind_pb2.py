# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sfeir/hivemind/protos/hivemind.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n$sfeir/hivemind/protos/hivemind.proto\x12\x15sfeir.hivemind.protos\x1a\x1cgoogle/api/annotations.proto"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t2i\n\x05\x41gent\x12`\n\x08SayHello\x12#.sfeir.hivemind.protos.HelloRequest\x1a!.sfeir.hivemind.protos.HelloReply"\x0c\x82\xd3\xe4\x93\x02\x06\x12\x04/sayb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "sfeir.hivemind.protos.hivemind_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _AGENT.methods_by_name["SayHello"]._options = None
    _AGENT.methods_by_name[
        "SayHello"
    ]._serialized_options = b"\202\323\344\223\002\006\022\004/say"
    _HELLOREQUEST._serialized_start = 93
    _HELLOREQUEST._serialized_end = 121
    _HELLOREPLY._serialized_start = 123
    _HELLOREPLY._serialized_end = 152
    _AGENT._serialized_start = 154
    _AGENT._serialized_end = 259
# @@protoc_insertion_point(module_scope)
