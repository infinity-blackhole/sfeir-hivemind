import os

import bentoml
from bentoml.io import Text

from sfeir.hivemind.runner import VertexAIRunnable

vertexai_runner = bentoml.Runner(
    VertexAIRunnable,
    name="sfeir-hivemind",
    runnable_init_params={
        "project": os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "location": "us-central1",
        "dataset_uri": os.environ["DEEP_LAKE_DATASET_URI"],
    },
)

svc = bentoml.Service("sfeir-hivemind", runners=[vertexai_runner])


@svc.api(input=Text(), output=Text())
async def classify(question: str, context: bentoml.Context) -> str:
    result = await vertexai_runner.predict.async_run(
        {"question": question, "chat_history": []}
    )
    return result["answer"]
