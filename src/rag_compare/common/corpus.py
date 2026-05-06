"""Loads the shared corpus used by all three patterns.

The included sample is small and Wikipedia-derived so it can ship in the repo.
Replace `data/raw/` with your own documents to try the patterns on a real use case.
"""

from pathlib import Path

from llama_index.core import Document, SimpleDirectoryReader

from rag_compare.common.config import get_settings


def load_corpus(path: Path | None = None) -> list[Document]:
    settings = get_settings()
    target = path or settings.data_raw
    if not any(target.iterdir()):
        raise FileNotFoundError(
            f"No documents in {target}. Run notebooks/00_setup_and_data.ipynb first."
        )
    return SimpleDirectoryReader(input_dir=str(target), recursive=True).load_data()
