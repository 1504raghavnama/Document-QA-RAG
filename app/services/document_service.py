import pymupdf
from app.models.document import DocumentPage
from pathlib import Path

class DocumentService:
    def extract_text(self, file_path: str)->list[DocumentPage]:
        try:
            document_name = Path(file_path).name
            document = pymupdf.open(file_path)

            pages: list[DocumentPage]=[]

            for page_number, page in enumerate(document):
                text = page.get_text("text").strip()

                if text:
                    pages.append(
                        DocumentPage(
                            document_name=document_name,
                            page_number=page_number+1,
                            text=text,
                        )
                    )
            if not pages:
                document.close()
                raise ValueError("No extractable text found in the PDF.")

            document.close()
            return pages
        
        except (pymupdf.FileDataError, pymupdf.FileNotFoundError) as exc:
            raise ValueError("Unable to read the PDF file.") from exc