"""LLM factory. Picks Anthropic or OpenAI based on the model name."""

from llama_index.core.llms import LLM

from rag_compare.common.config import get_settings


def get_llm(model: str | None = None) -> LLM:
    settings = get_settings()
    name = model or settings.llm_model

    if name.startswith("claude"):
        from llama_index.llms.anthropic import Anthropic

        return Anthropic(model=name, api_key=settings.anthropic_api_key)

    from llama_index.llms.openai import OpenAI

    return OpenAI(model=name, api_key=settings.openai_api_key)
