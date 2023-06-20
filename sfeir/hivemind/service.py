import os

import bentoml
from bentoml.io import Text

from sfeir.hivemind.runner import VertexAIRunnable

vertexai_runner = bentoml.Runner(
    VertexAIRunnable,
    name="sfeir-hivemind",
    runnable_init_params={
        "project": os.environ.get("VERTEX_AI_PROJECT"),
        "location": os.environ.get("VERTEX_AI_LOCATION"),
        "dataset_uri": os.environ["DEEP_LAKE_DATASET_URI"],
    },
)

svc = bentoml.Service("sfeir-hivemind", runners=[vertexai_runner])


@svc.api(input=Text(), output=Text())
async def predict(question: str, context: bentoml.Context) -> str:
    result = await vertexai_runner.predict.async_run(
        {"question": question, "chat_history": []}
    )
    return result["answer"]
