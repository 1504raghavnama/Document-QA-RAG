from app.core.config import settings
from app.models.document import DocumentChunk, DocumentPage


class ChunkingService:
    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.chunk_size = (
            settings.chunk_size if chunk_size is None else chunk_size
        )

        self.chunk_overlap = (
            settings.chunk_overlap
            if chunk_overlap is None
            else chunk_overlap
        )

        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

    def chunk_pages(self, pages: list[DocumentPage]) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        for page in pages:
            chunks.extend(self._chunk_page(page))

        return chunks

    def _chunk_page(self, page: DocumentPage) -> list[DocumentChunk]:
        words = page.text.split()
        chunks: list[DocumentChunk] = []

        current_words: list[str] = []
        chunk_number = 1

        for word in words:
            candidate_words = current_words + [word]
            candidate_text = " ".join(candidate_words)

            if current_words and len(candidate_text) > self.chunk_size:
                chunks.append(
                    DocumentChunk(
                        chunk_id=(
                            f"{page.document_name}-"
                            f"{page.page_number}-"
                            f"{chunk_number}"
                        ),
                        document_name=page.document_name,
                        page_number=page.page_number,
                        text=" ".join(current_words),
                    )
                )

                overlap_words: list[str] = []
                overlap_length = 0

                for previous_word in reversed(current_words):
                    word_length = len(previous_word)

                    if overlap_words:
                        word_length += 1

                    if overlap_length + word_length > self.chunk_overlap:
                        break

                    overlap_words.insert(0, previous_word)
                    overlap_length += word_length

                current_words = overlap_words

            current_words.append(word)
            chunk_number += 1

        if current_words:
            chunks.append(
                DocumentChunk(
                    chunk_id=(
                        f"{page.document_name}-"
                        f"{page.page_number}-"
                        f"{chunk_number}"
                    ),
                    document_name=page.document_name,
                    page_number=page.page_number,
                    text=" ".join(current_words),
                )
            )

        return chunks