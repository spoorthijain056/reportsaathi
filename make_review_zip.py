from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path.cwd()
output = root.parent / "reportsaathi-review.zip"

excluded = {
    ".git", ".venv", "venv", "node_modules",
    "__pycache__", ".pytest_cache", ".ruff_cache"
}

with ZipFile(output, "w", ZIP_DEFLATED) as archive:
    for file in root.rglob("*"):
        relative = file.relative_to(root)

        if any(part in excluded for part in relative.parts):
            continue

        if not file.is_file():
            continue

        if file.name == ".env" or file.name.startswith(".env."):
            continue

        archive.write(file, relative)

print(f"ZIP created: {output}")
