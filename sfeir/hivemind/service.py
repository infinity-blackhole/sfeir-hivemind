import os

import bentoml
import vertexai
from bentoml.io import Text
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI
from langchain.vectorstores import DeepLake

llm = VertexAI()
embeddings = VertexAIEmbeddings()

vectorstore = DeepLake(
    dataset_path="gcs://shikanime-studio-labs-hivemind-deep-lake-dataset/books/",
    embedding_function=embeddings,
    read_only=True,
)

qa = ConversationalRetrievalChain.from_llm(
    llm,
    vectorstore.as_retriever(),
    return_source_documents=True,
    verbose=True,
)

svc = bentoml.Service("sfeir-hivemind")


@svc.on_startup
async def vertexai_init_on_startup(context: bentoml.Context):
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", None)
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", None)
    vertexai.init(project=project, location=location)


@svc.api(input=Text(), output=Text())
async def classify(question: str) -> str:
    result = qa({"question": question, "chat_history": []})
    return result["answer"]
