import os
from typing import Any, Literal

import bentoml
from bentoml.io import Text
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI
from langchain.vectorstores import DeepLake


class VertexAIRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu", "nvidia.com/gpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(
        self, project: str, location: Literal["us-central1"], dataset_uri: str
    ):
        self.llm = VertexAI(project=project, location=location)
        self.embeddings = VertexAIEmbeddings(project=project, location=location)
        self.vectorstore = DeepLake(
            dataset_path=dataset_uri,
            embedding_function=self.embeddings,
            read_only=True,
        )
        self.chain = ConversationalRetrievalChain.from_llm(
            self.llm,
            self.vectorstore.as_retriever(),
            return_source_documents=True,
            verbose=True,
        )

    @bentoml.Runnable.method(batchable=False)
    def predict(
        self,
        inputs: dict[str, Any],
    ):
        return self.chain(inputs)


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
