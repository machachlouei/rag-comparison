"""Downloads a curated Wikipedia corpus into data/raw/.

Domain: AI labs and large language models. Chosen because the articles share
many entities (companies, founders, models, papers), have plenty of exact
terms (model names, dates, paper titles), and let us write a meaningful
unanswerable question.

Idempotent: skips files that already exist.
"""

from pathlib import Path

import wikipediaapi

from rag_compare.common.config import get_settings

STARTER_ARTICLES: list[str] = [
    # Architecture & techniques
    "Large language model",
    "Transformer (deep learning architecture)",
    "Attention Is All You Need",
    "Reinforcement learning from human feedback",
    "Retrieval-augmented generation",
    # Labs
    "OpenAI",
    "Anthropic",
    "Google DeepMind",
    "Mistral AI",
    # Models
    "GPT-4",
    "Claude (language model)",
    "Gemini (language model)",
    "Llama (language model)",
    # People
    "Sam Altman",
    "Dario Amodei",
    "Demis Hassabis",
    "Geoffrey Hinton",
    "Ilya Sutskever",
]

USER_AGENT = "rag-compare-edu/0.1 (https://github.com/example/rag-comparison)"


def fetch_starter_corpus(
    target: Path | None = None,
    articles: list[str] | None = None,
    overwrite: bool = False,
) -> list[Path]:
    """Download articles into target dir as plain-text files. Returns paths written."""
    cfg = get_settings()
    target = target or cfg.data_raw
    target.mkdir(parents=True, exist_ok=True)
    titles = articles or STARTER_ARTICLES

    wiki = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language="en")

    written = []
    for title in titles:
        out = target / f"{_slug(title)}.txt"
        if out.exists() and not overwrite:
            written.append(out)
            continue
        page = wiki.page(title)
        if not page.exists():
            print(f"[skip] no Wikipedia page for: {title}")
            continue
        out.write_text(f"# {page.title}\n\n{page.text}", encoding="utf-8")
        written.append(out)
        print(f"[ok]   {title} -> {out.name}")
    return written


def _slug(title: str) -> str:
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return "".join(c if c in keep else "_" for c in title).strip("_")
