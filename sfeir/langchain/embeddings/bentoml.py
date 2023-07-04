from typing import Any, Dict, List

import bentoml
from langchain.embeddings.base import Embeddings
from pydantic import BaseModel, Extra, Field


class BentoMLEmbeddings(BaseModel, Embeddings):
    """Wrapper around BentoML runner.

    To use, you should have the ``bentoml`` python package installed.

    Example:
        .. code-block:: python

            from langchain.embeddings import BentoMLEmbeddings

            model_name = "sentence-transformers"
            encode_kwargs = {'normalize_embeddings': False}
            hf = BentoMLEmbeddings(
                model_name=model_name,
                encode_kwargs=encode_kwargs
            )
    """

    client: Any  #: :meta private:

    model_tag: str
    """Key word arguments to pass to the model."""
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass when calling the `encode` method of the model."""

    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        self.client = bentoml.pytorch.get(self.model_tag).to_runner()

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @property
    def runner(self) -> bentoml.Runner:
        """
        Get the underlying bentoml.Runner instance for integration with BentoML.

        Example:
        .. code-block:: python

            embeddings = bentoml(
                model_tag='sentence-transformers',
            )
            svc = bentoml.Service("langchain-bentoml", runners=[embeddings.runner])
        """
        if self.client is None:
            raise ValueError("BentoML must be initialized locally with 'model_name'")
        return self.client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a BentoML model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.client.encode.run(texts, **self.encode_kwargs)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a BentoML model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        embedding = self.client.encode.run(text, **self.encode_kwargs)
        return embedding.tolist()
