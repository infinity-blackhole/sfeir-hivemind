import bentoml
from bentoml.io import Text, NumpyNdarray


embeddings_runner = bentoml.pytorch.get("sfeir-hivemind-all-mpnet-base-v2").to_runner()

svc = bentoml.Service("sfeir-hivemind-embeddings", runners=[embeddings_runner])


@svc.api(input=Text(), output=NumpyNdarray())
async def encode(text: str) -> str:
    return embeddings_runner.encode.run(text)
