# 03 — Tradeoffs

Filled in by [`notebooks/05_evaluation_and_costs.ipynb`](../notebooks/05_evaluation_and_costs.ipynb) on the included corpus. Numbers below are *expected ranges* you should reproduce yourself.

## Quality (RAGAS, golden set ~30 questions)

| Metric | Baseline RAG | KG-RAG | Hybrid RAG | Agentic RAG |
|---|---|---|---|---|
| Faithfulness | ~0.75 | ~0.85 | ~0.85 | ~0.90 |
| Answer relevance | ~0.80 | ~0.82 | ~0.88 | ~0.90 |
| Context recall | ~0.65 | ~0.80 | ~0.85 | ~0.88 |
| Multi-hop accuracy | low | **high** | medium | **high** |

## Cost & latency (per query)

| Dimension | KG-RAG | Hybrid RAG | Agentic RAG |
|---|---|---|---|
| Indexing $ | **High** (LLM extracts triples) | Low | Low |
| Indexing time | **High** | Low | Low |
| Query latency | Medium (one DB roundtrip) | Low | **High** (multiple LLM calls) |
| $ per query | Low | Low | **High** (3–10× LLM calls) |
| Infra footprint | Graph DB + vector DB | Vector DB + BM25 | Vector DB (+ tools) |

## Operational

| | KG-RAG | Hybrid RAG | Agentic RAG |
|---|---|---|---|
| Debuggability | Good (graph is inspectable) | Good (rank lists) | **Hard** (agent traces) |
| Failure modes | Bad triples, missed entities | Stop-word-heavy queries | Loops, tool misuse |
| Update cost | Re-extract on doc change | Re-embed/re-index chunk | Same as underlying tools |
| Determinism | High | High | Low |

## When the extra complexity is worth it

- **Hybrid RAG** is almost always worth it over baseline. Default choice.
- **KG-RAG** pays off when the *structure* of the answer matters (relationships, hierarchies, multi-hop).
- **Agentic RAG** pays off when *one retriever isn't enough* — heterogeneous sources, dynamic decisions, follow-up questions.

You can also **stack** them: an agent whose tools are a hybrid retriever and a KG retriever is a common production pattern.
