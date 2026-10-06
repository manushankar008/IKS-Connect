from pypdf import PdfReader

pdf_path = "data/sources/kerala/culture/kerala_economic_review_2024.pdf"
output_path = "data/extracted/kerala/kerala_economic_review_2024.txt"

reader = PdfReader(pdf_path)

with open(output_path, "w", encoding="utf-8") as file:

    for i, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text:
            file.write(f"\n\n--- PAGE {i + 1} ---\n\n")
            file.write(page_text)

print("PDF text extracted successfully!")
print("Total pages:", len(reader.pages))