import re

input_path = "data/extracted/kerala/kerala_economic_review_2024.txt"
output_path = "data/extracted/kerala/kerala_economic_review_2024_clean.txt"

with open(input_path, "r", encoding="utf-8") as file:
    text = file.read()

# Remove excessive spaces at the beginning/end of lines
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

    # Remove multiple spaces
    line = re.sub(r"\s+", " ", line)

    cleaned_lines.append(line)

# Remove too many consecutive blank lines
cleaned_text = "\n".join(cleaned_lines)
cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

with open(output_path, "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Text cleaned successfully!")
print("Output:", output_path)