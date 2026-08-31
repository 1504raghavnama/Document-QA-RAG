from pydantic import BaseModel

class DocumentPage(BaseModel):
    document_name: str
    page_number: int
    text: str