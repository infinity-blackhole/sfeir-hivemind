import os
from typing import Any

import bentoml
from bentoml.io import JSON, Text

from sfeir.hivemind.io import Output
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


@svc.api(input=Text(), output=JSON(pydantic_model=Output))
def predict(question: str, context: bentoml.Context) -> dict[str, Any]:
    result = vertexai_runner.predict.run({"question": question, "chat_history": []})
    return {
        "question": result["question"],
        "answer": result["answer"],
        "source_documents": [
            {
                "page_content": doc.page_content,
                "source": doc.metadata["source"],
                "title": doc.metadata["title"],
                "page": doc.metadata["page"],
            }
            for doc in result["source_documents"]
        ],
    }
