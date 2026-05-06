# 01 — Concepts

Vocabulary you need before reading the rest of the docs.

## Baseline RAG (the thing all three patterns build on)

1. **Index** — chunk documents → embed → store vectors
2. **Retrieve** — embed query → nearest-neighbor search → top-k chunks
3. **Generate** — stuff chunks into prompt → LLM answers

Failure modes this leaves on the table:
- Misses exact-term matches (vector search is fuzzy)
- Can't answer multi-hop questions ("X's competitor's CEO")
- Treats all sources the same (web docs ≈ tickets ≈ specs)
- One-shot: no refinement when retrieval is wrong

The three patterns each address a different subset.

## KG-RAG (Knowledge Graph RAG)

Build a graph of **entities** (nodes) and **relationships** (edges) extracted from the corpus. At query time, retrieve a *subgraph* relevant to the question — not just chunks.

- Index: NER + relation extraction → triples → graph DB (Neo4j)
- Retrieve: entity linking on query → graph traversal (Cypher) → subgraph + linked text
- Generate: LLM reasons over the subgraph

**Pays off** when answers depend on relationships rather than passages.

## Hybrid RAG

Run **two retrievers in parallel** (dense + sparse), fuse the results, then rerank.

- **Dense**: embedding similarity — captures meaning
- **Sparse (BM25)**: term overlap — captures exact tokens (codes, IDs, jargon)
- **Fusion**: Reciprocal Rank Fusion (RRF) or score normalization
- **Rerank**: cross-encoder scores each (query, doc) pair more accurately than bi-encoder retrieval

**Pays off** almost universally — the cheapest accuracy upgrade over baseline RAG.

## Agentic RAG

An LLM-driven **agent** treats retrieval as a tool. It can:
- Decompose the query into sub-questions
- Pick which index/tool to call (vector? graph? web? SQL?)
- Inspect results, decide whether to retry/refine
- Loop until it has enough evidence

Implemented as a state machine (LangGraph) or a ReAct loop.

**Pays off** when sources are heterogeneous or queries are multi-step.

## Cross-cutting concepts

- **Chunking**: how you split documents. Affects all three.
- **Embeddings**: dense vector representation. Used by baseline, hybrid, and often agentic.
- **Reranking**: a second-stage scorer. Used by hybrid; optional for the others.
- **Evaluation**: faithfulness (no hallucination), answer relevance, context recall/precision. We use RAGAS.
