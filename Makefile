.PHONY: all
all: sync gen

gen:
	@python -m grpc_tools.protoc \
		-I . \
		--pyi_out=. \
		--python_out=. \
		--grpc_python_out=. \
		./sfeir/hivemind/protos/*.proto

.PHONY: sync
sync:
	@hatch dep show requirements --project-only > requirements.txt