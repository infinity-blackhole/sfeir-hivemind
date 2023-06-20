from typing import Any

import bentoml
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI
from langchain.vectorstores import DeepLake


class VertexAIRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu", "nvidia.com/gpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self, project: str, location: str, dataset_uri: str):
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
    def predict(self, inputs: dict[str, Any]):
        return self.chain(inputs)
