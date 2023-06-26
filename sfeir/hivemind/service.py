import os
from typing import Any

import bentoml
from bentoml.io import JSON
from langchain.memory.chat_message_histories import FirestoreChatMessageHistory

from sfeir.hivemind.runner import VertexAIRunnable
from sfeir.hivemind.schema import (
    QuestionAnsweringRequest,
    QuestionAnsweringResponse,
    SourceDocument,
)

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
    result = await vertexai_runner.predict.async_run(
        {"question": qa.question, "chat_history": chat_message_history.messages}
    )
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
