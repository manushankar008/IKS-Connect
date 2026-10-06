import os
import re


input_folder = "data/extracted/kerala_clean"
output_folder = "data/chunks/kerala"

os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(
    output_folder,
    "kerala_chunks.txt"
)


chunk_size = 1500
overlap = 200

chunk_number = 0


with open(output_path, "w", encoding="utf-8") as output:

    for root, folders, files in os.walk(input_folder):

        for file in files:

            if not file.lower().endswith(".txt"):
                continue

            input_path = os.path.join(root, file)

            # Get category
            relative_path = os.path.relpath(
                root,
                input_folder
            )

            category = relative_path

            print("\nChunking:", file)

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split using page markers
            pages = re.split(
                r"--- PAGE (\d+) ---",
                text
            )

            for i in range(1, len(pages), 2):

                page_number = pages[i]
                page_text = pages[i + 1].strip()

                if not page_text:
                    continue

                start = 0

                while start < len(page_text):

                    end = start + chunk_size

                    chunk_text = page_text[start:end]

                    output.write(
                        f"\n--- CHUNK {chunk_number} ---\n"
                    )

                    output.write(
                        f"SOURCE: {file}\n"
                    )

                    output.write(
                        f"CATEGORY: {category}\n"
                    )

                    output.write(
                        f"STATE: Kerala\n"
                    )

                    output.write(
                        f"PAGE: {page_number}\n"
                    )

                    output.write(
                        f"TEXT:\n{chunk_text}\n"
                    )

                    chunk_number += 1

                    # Move forward while keeping overlap
                    start = end - overlap


print("\nAll text files chunked successfully!")

print("Total chunks:", chunk_number)

print("Saved:", output_path)