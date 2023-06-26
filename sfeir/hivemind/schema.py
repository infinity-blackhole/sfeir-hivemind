from pydantic import BaseModel


class QuestionAnsweringRequest(BaseModel):
    question: str
    chat_history: list[str] = []


class SourceDocument(BaseModel):
    page_content: str
    source: str
    title: str
    page: int


class QuestionAnsweringResponse(BaseModel):
    question: str
    answer: str
    source_documents: list[SourceDocument]
