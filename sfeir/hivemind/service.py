import os

import bentoml
from bentoml.io import JSON
from langchain.llms.openllm import OpenLLM
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import FirestoreChatMessageHistory
from langchain.vectorstores import DeepLake

from sfeir.hivemind.schema import (
    QuestionAnsweringRequest,
    QuestionAnsweringResponse,
    SourceDocument,
)
from sfeir.langchain.embeddings.hivemind import HivemindEmbeddings

llm = OpenLLM(server_url=os.environ.get("OPENLLM_SERVER_URL", "http://localhost:3000"))
embeddings = HivemindEmbeddings(
    server_url=os.environ.get("EMBEDDINGS_SERVER_URL", "http://localhost:3001")
)

vectorstore = DeepLake(
    dataset_path=os.environ["DEEP_LAKE_DATASET_URI"],
    embedding_function=embeddings,
    read_only=True,
)

chain = ConversationalRetrievalChain.from_llm(
    llm,
    vectorstore.as_retriever(),
    return_source_documents=True,
)

svc = bentoml.Service("sfeir_hivemind", runners=[])


@svc.api(
    input=JSON(pydantic_model=QuestionAnsweringRequest),
    output=JSON(pydantic_model=QuestionAnsweringResponse),
)
async def predict(qa: QuestionAnsweringRequest) -> QuestionAnsweringResponse:
    chat_message_history = FirestoreChatMessageHistory(
        collection_name="chat_history",
        session_id=qa.session_id,
        user_id=qa.user_id,
    )
    result = chain(
        {"question": qa.question, "chat_history": chat_message_history.messages}
    )
    chat_message_history.add_user_message(qa.question)
    chat_message_history.add_ai_message(result["answer"])
    return QuestionAnsweringResponse(
        question=result["question"],
        answer=result["answer"],
        source_documents=[
            SourceDocument(
                page_content=doc.page_content,
                source=doc.metadata["source"],
                title=doc.metadata["title"],
                page=doc.metadata["page"],
            )
            for doc in result["source_documents"]
        ],
    )
