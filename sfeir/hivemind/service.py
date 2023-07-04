import os
from typing import Any, Dict, List

import bentoml
from bentoml.io import JSON
from langchain.embeddings.base import Embeddings
from langchain.memory.chat_message_histories import FirestoreChatMessageHistory
from pydantic import BaseModel, Extra, Field

from sfeir.hivemind.runner import VertexAIRunnable
from sfeir.hivemind.schema import (
    QuestionAnsweringRequest,
    QuestionAnsweringResponse,
    SourceDocument,
)


class BentoEmbeddings(BaseModel, Embeddings):
    """BentoML Runner."""

    runner: Any
    """Path to store models.
    Can be also set by SENTENCE_TRANSFORMERS_HOME environment variable."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass to the model."""
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass when calling the `encode` method of the model."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a HuggingFace transformer model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.runner.encode.run(texts, **self.encode_kwargs)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a HuggingFace transformer model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        embedding = self.runner.encode.run(text, **self.encode_kwargs)
        return embedding.tolist()


embedding_runner = bentoml.pytorch.get("sentence-transformers").to_runner()

vertexai_runner = bentoml.Runner(
    VertexAIRunnable,
    name="sfeir-hivemind",
    runnable_init_params={
        "project": os.environ.get("VERTEX_AI_PROJECT"),
        "location": os.environ.get("VERTEX_AI_LOCATION"),
        "dataset_uri": os.environ["DEEP_LAKE_DATASET_URI"],
        "embeddings": BentoEmbeddings(runner=embedding_runner),
    },
)

svc = bentoml.Service("sfeir-hivemind", runners=[vertexai_runner, embedding_runner])


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
