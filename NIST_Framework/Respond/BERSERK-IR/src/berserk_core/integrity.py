import hashlib
from pathlib import Path


def calculate_sha256(file_path: Path) -> str:
    """
    Calculate the SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def write_hash_file(file_path: Path) -> Path:
    """
    Write a SHA-256 integrity record beside the artifact.
    """

    digest = calculate_sha256(file_path)

    hash_file = file_path.with_suffix(
        file_path.suffix + ".sha256"
    )

    hash_file.write_text(
        f"{digest}  {file_path.name}\n",
        encoding="utf-8"
    )

    return hash_file
