from pydantic import BaseModel


class SourceDocument(BaseModel):
    page_content: str
    source: str
    title: str
    page: int


class Output(BaseModel):
    question: str
    answer: str
    source_documents: list[SourceDocument]
