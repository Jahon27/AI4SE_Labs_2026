import json
from pathlib import Path


SOURCE_REPOSITORY = Path(__file__).parent.parent.parent.parent / "AI4SE_Playground"
OUTPUT_FILE = Path(__file__).parent / "chunks.json"
CHUNK_SIZE = 50

SOURCE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".h", ".cpp",
    ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt",
    ".kts", ".sh", ".sql", ".html", ".css", ".scss", ".xml", ".yaml",
    ".yml", ".toml",
}
SKIPPED_DIRECTORIES = {
    ".git", "__pycache__", ".venv", "venv", "node_modules", "dist",
    "build", "coverage",
}
GENERATED_NAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
}


def is_binary(path):
    with path.open("rb") as file:
        return b"\x00" in file.read(4096)


def should_skip(path):
    if any(directory in SKIPPED_DIRECTORIES for directory in path.parts):
        return True
    if path.name in GENERATED_NAMES or path.name.endswith(".min.js"):
        return True
    return path.suffix.lower() not in SOURCE_EXTENSIONS


def create_chunks():
    chunks = []

    for path in sorted(SOURCE_REPOSITORY.rglob("*")):
        if not path.is_file() or should_skip(path) or is_binary(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        relative_path = path.relative_to(SOURCE_REPOSITORY).as_posix()
        for start in range(0, len(lines), CHUNK_SIZE):
            chunks.append(
                {
                    "file_path": relative_path,
                    "chunk_id": start // CHUNK_SIZE + 1,
                    "content": "\n".join(lines[start:start + CHUNK_SIZE]),
                }
            )

    return chunks


def main():
    if not SOURCE_REPOSITORY.is_dir():
        raise FileNotFoundError(f"Repository not found: {SOURCE_REPOSITORY}")

    chunks = create_chunks()
    OUTPUT_FILE.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"Created {OUTPUT_FILE} with {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
