import os
from pypdf import PdfReader


source_folder = "data/sources/kerala"
output_folder = "data/extracted/kerala"


for root, folders, files in os.walk(source_folder):

    for file in files:

        if file.lower().endswith(".pdf"):

            pdf_path = os.path.join(root, file)

            # Find the category folder
            relative_path = os.path.relpath(root, source_folder)

            output_category_folder = os.path.join(
                output_folder,
                relative_path
            )

            os.makedirs(output_category_folder, exist_ok=True)

            # Create output filename
            filename = os.path.splitext(file)[0] + ".txt"

            output_path = os.path.join(
                output_category_folder,
                filename
            )

            print("\nExtracting:", file)

            reader = PdfReader(pdf_path)

            with open(output_path, "w", encoding="utf-8") as output_file:

                for i, page in enumerate(reader.pages):

                    page_text = page.extract_text()

                    if page_text:

                        output_file.write(
                            f"\n\n--- PAGE {i + 1} ---\n\n"
                        )

                        output_file.write(page_text)

            print("Saved:", output_path)
            print("Pages:", len(reader.pages))


print("\nAll PDFs extracted successfully!")