# RAG Patterns Compared: KG-RAG vs Hybrid RAG vs Agentic RAG

[![CI](https://github.com/machachlouei/rag-comparison/actions/workflows/ci.yml/badge.svg)](https://github.com/machachlouei/rag-comparison/actions/workflows/ci.yml)

An educational repo that builds the **same Q&A system three ways** so you can see, run, and measure the differences.

## Patterns covered

| Pattern | Core idea | Strongest when |
|---|---|---|
| **KG-RAG** | Retrieve from a knowledge graph; answer with structured facts and relationships | Multi-hop reasoning, entity-rich domains (biomed, finance, legal) |
| **Hybrid RAG** | Fuse dense (embeddings) + sparse (BM25) retrieval, then rerank | Mixed terminology, exact terms matter, broad corpora |
| **Agentic RAG** | An agent decides *which* tool/index to query, refines, and retries | Heterogeneous sources, complex queries, tool use needed |

## Learning path

1. Read [`docs/01-concepts.md`](docs/01-concepts.md)
2. Run [`notebooks/00_setup_and_data.ipynb`](notebooks/00_setup_and_data.ipynb) to load the shared corpus
3. Walk through patterns one-by-one: notebooks `01`, `02`, `03`
4. See them on the *same questions* in [`notebooks/04_side_by_side_comparison.ipynb`](notebooks/04_side_by_side_comparison.ipynb)
5. Measure quality, latency, and cost in [`notebooks/05_evaluation_and_costs.ipynb`](notebooks/05_evaluation_and_costs.ipynb)

## Quickstart

```bash
# 1. Install (uses uv; falls back to pip)
uv sync   # or: pip install -e ".[dev]"

# 2. Copy env template and add API keys
cp .env.example .env

# 3. Start backing services (Neo4j + Qdrant)
docker compose up -d

# 4. Launch notebooks
jupyter lab
```

## Repo layout

```
data/        Source corpus + processed artifacts
docs/        Concepts, architecture diagrams, tradeoffs, decision guide
src/         Python package implementing each pattern + shared utilities
notebooks/   Hands-on walkthroughs and the side-by-side comparison
tests/       Smoke tests so notebooks don't rot
```

## When to use which pattern

See [`docs/04-when-to-use.md`](docs/04-when-to-use.md) for a decision tree. Short version:

- Need **multi-hop joins across entities**? → KG-RAG
- Need **best general retrieval quality** with low effort? → Hybrid RAG
- Need to **route across multiple sources or refine queries**? → Agentic RAG

## License

MIT. Corpus licenses noted in [`data/README.md`](data/README.md).
