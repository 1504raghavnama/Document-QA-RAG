from app.models.document import DocumentPage
from app.services.chunking_service import ChunkingService


def test_chunk_pages():
    pages = [
        DocumentPage(
            document_name="chunking-test.pdf",
            page_number=1,
            text=(
                "Artificial intelligence is transforming many industries. "
                "Machine learning allows computers to learn patterns from data. "
                "Retrieval augmented generation combines information retrieval "
                "with large language models."
            ),
        ),
        DocumentPage(
            document_name="chunking-test.pdf",
            page_number=2,
            text=(
                "Chunking is an important step because it determines how "
                "documents are divided before embeddings are created. "
                "Good chunking improves retrieval quality."
            ),
        ),
    ]

    chunking_service = ChunkingService(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunking_service.chunk_pages(pages)

    assert len(chunks) == 5

    for chunk in chunks:
        assert chunk.document_name == "chunking-test.pdf"
        assert chunk.page_number in (1, 2)
        assert chunk.text
        assert len(chunk.text) <= 100
        assert chunk.chunk_id


def test_invalid_chunk_size():
    try:
        ChunkingService(chunk_size=0, chunk_overlap=20)
        assert False
    except ValueError:
        assert True


def test_invalid_chunk_overlap():
    try:
        ChunkingService(chunk_size=100, chunk_overlap=100)
        assert False
    except ValueError:
        assert True


def test_empty_page_is_ignored():
    page = DocumentPage(
        document_name="empty.pdf",
        page_number=1,
        text="",
    )

    chunking_service = ChunkingService()

    chunks = chunking_service.chunk_pages([page])

    assert chunks == []


def test_short_text_creates_one_chunk():
    page = DocumentPage(
        document_name="short.pdf",
        page_number=1,
        text="This is a short document.",
    )

    chunking_service = ChunkingService(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunking_service.chunk_pages([page])

    assert len(chunks) == 1
    assert chunks[0].text == "This is a short document."
    assert chunks[0].page_number == 1


def test_multiple_pages_preserve_page_numbers():
    pages = [
        DocumentPage(
            document_name="multi-page.pdf",
            page_number=1,
            text="Content from page one.",
        ),
        DocumentPage(
            document_name="multi-page.pdf",
            page_number=2,
            text="Content from page two.",
        ),
    ]

    chunking_service = ChunkingService()

    chunks = chunking_service.chunk_pages(pages)

    assert len(chunks) == 2
    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 2


def test_overlap_preserves_previous_words():
    page = DocumentPage(
        document_name="overlap.pdf",
        page_number=1,
        text=(
            "Artificial intelligence is transforming many industries "
            "and machine learning is changing how software is developed."
        ),
    )

    chunking_service = ChunkingService(
        chunk_size=60,
        chunk_overlap=20,
    )

    chunks = chunking_service.chunk_pages([page])

    assert len(chunks) > 1

    first_words = chunks[0].text.split()
    second_words = chunks[1].text.split()

    assert any(word in second_words for word in first_words[-3:])

def test_chunking_service_uses_settings():
    chunking_service = ChunkingService()

    assert chunking_service.chunk_size == 500
    assert chunking_service.chunk_overlap == 50