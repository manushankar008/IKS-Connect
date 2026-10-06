import os
import re


input_folder = "data/extracted/kerala"
output_folder = "data/extracted/kerala_clean"


for root, folders, files in os.walk(input_folder):

    for file in files:

        if file.lower().endswith(".txt"):

            input_path = os.path.join(root, file)

            # Keep the same folder structure
            relative_path = os.path.relpath(root, input_folder)

            output_category_folder = os.path.join(
                output_folder,
                relative_path
            )

            os.makedirs(output_category_folder, exist_ok=True)

            output_path = os.path.join(
                output_category_folder,
                file
            )

            print("\nCleaning:", file)

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            lines = text.splitlines()

            cleaned_lines = []

            for line in lines:

                line = line.strip()

                # Keep page markers
                if line.startswith("--- PAGE"):
                    cleaned_lines.append("")
                    cleaned_lines.append(line)
                    cleaned_lines.append("")
                    continue

                # Remove excessive spaces
                line = re.sub(r"\s+", " ", line)

                if line:
                    cleaned_lines.append(line)

            cleaned_text = "\n".join(cleaned_lines)

            # Remove too many blank lines
            cleaned_text = re.sub(
                r"\n{3,}",
                "\n\n",
                cleaned_text
            )

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print("Saved:", output_path)


print("\nAll text files cleaned successfully!")