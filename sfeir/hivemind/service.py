import os
from typing import cast

import bentoml
import vertexai
from bentoml.io import Text
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI
from langchain.vectorstores import DeepLake

svc = bentoml.Service("sfeir-hivemind")


@svc.on_startup
async def on_startup(context: bentoml.Context):
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    dataset_path = os.environ.get("DEEP_LAKE_DATASET_URI")
    if dataset_path is None:
        raise bentoml.exceptions.InvalidArgument(
            "DEEP_LAKE_DATASET_URI environment variable not set"
        )

    vertexai.init(project=project, location=location)

    llm = context.state["llm"] = VertexAI()
    embeddings = context.state["embeddings"] = VertexAIEmbeddings()
    vectorstore = context.state["vectorstore"] = DeepLake(
        dataset_path=dataset_path,
        embedding_function=embeddings,
        read_only=True,
    )
    _chain = context.state["chain"] = ConversationalRetrievalChain.from_llm(
        llm,
        vectorstore.as_retriever(),
        return_source_documents=True,
        verbose=True,
    )


@svc.api(input=Text(), output=Text())
async def classify(question: str, context: bentoml.Context) -> str:
    chain = cast(ConversationalRetrievalChain, context.state.get("chain"))
    if chain is None:
        raise bentoml.exceptions.ServiceUnavailable("Model not ready")
    result = chain({"question": question, "chat_history": []})
    return result["answer"]
