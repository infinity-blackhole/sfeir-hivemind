from pydantic import BaseModel


class QuestionAnsweringRequest(BaseModel):
    question: str
    session_id: str
    user_id: str


class SourceDocument(BaseModel):
    page_content: str
    source: str
    title: str
    page: int


class QuestionAnsweringResponse(BaseModel):
    question: str
    answer: str
    source_documents: list[SourceDocument]
