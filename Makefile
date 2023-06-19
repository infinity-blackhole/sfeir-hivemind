.PHONY: all
all: sync gen containers

gen:
	@python -m grpc_tools.protoc \
		-I . \
		-I third_party/googleapis \
		--include_imports \
		--include_source_info \
		--descriptor_set_out=sfeir/hivemind/protos/proto.pb \
		--pyi_out=. \
		--python_out=. \
		--grpc_python_out=. \
		sfeir/hivemind/protos/*.proto

.PHONY: sync
sync:
	@hatch dep show requirements --project-only > requirements.txt

.PHONY: containers
containers:
	@skaffold build