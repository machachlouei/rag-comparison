"""Smoke tests so the package keeps importing as we evolve it.

These don't hit external services — they only verify the modules load and
the public surface is intact. Run with: pytest tests/
"""


def test_common_imports():
    from rag_compare.common import (
        Settings,
        chunk_documents,
        get_embedder,
        get_llm,
        get_settings,
        load_corpus,
    )

    assert all(callable(x) for x in [chunk_documents, get_embedder, get_llm, get_settings, load_corpus])
    assert Settings is not None


def test_pipeline_classes_importable():
    from rag_compare.agentic_rag import AgenticRagPipeline
    from rag_compare.hybrid_rag import HybridRagPipeline
    from rag_compare.kg_rag import KGRagPipeline

    assert KGRagPipeline is not None
    assert HybridRagPipeline is not None
    assert AgenticRagPipeline is not None


def test_eval_surface():
    from rag_compare.eval import GOLDEN_QUESTIONS, GoldenItem, run_eval

    assert callable(run_eval)
    assert len(GOLDEN_QUESTIONS) > 0
    assert all(isinstance(q, GoldenItem) for q in GOLDEN_QUESTIONS)
