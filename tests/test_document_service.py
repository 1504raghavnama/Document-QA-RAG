from app.services.document_service import DocumentService

document_service=DocumentService()

pages=document_service.extract_text("tests/sample.pdf")

print(f"pages extracted {len(pages)}")

for page in pages:
    print(f"\nDocument: {page.document_name}")
    print(f"\nPage {page.page_number}:")
    print(page.text)

try:
    document_service.extract_text("tests/missing.pdf")
except ValueError as exc:
    print(f"\nError handled correctly: {exc}")

try:
    document_service.extract_text("tests/empty.pdf")
except ValueError as exc:
    print(f"Empty PDF handled correctly: {exc}")