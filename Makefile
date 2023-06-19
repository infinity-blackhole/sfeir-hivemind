.PHONY: all
all: sync gen containers

gen:
	@bentoml build

.PHONY: containers
containers:
	@skaffold build