"""Embedding factory. OpenAI by default; HuggingFace local fallback."""

from llama_index.core.embeddings import BaseEmbedding

from rag_compare.common.config import get_settings


def get_embedder(model: str | None = None) -> BaseEmbedding:
    settings = get_settings()
    name = model or settings.embedding_model

    if name.startswith("text-embedding"):
        from llama_index.embeddings.openai import OpenAIEmbedding

        return OpenAIEmbedding(model=name, api_key=settings.openai_api_key)

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    return HuggingFaceEmbedding(model_name=name)
