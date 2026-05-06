# 02 — Architecture

Side-by-side pipelines. All three start from the same corpus.

## KG-RAG

```mermaid
flowchart LR
    A[Documents] --> B[Chunk]
    B --> C[NER + Relation Extraction<br/>LLM-powered]
    C --> D[(Neo4j<br/>entities + edges)]
    B --> E[(Vector store<br/>chunk embeddings)]
    Q[Question] --> F[Entity linking]
    F --> G[Cypher traversal]
    D --> G
    G --> H[Subgraph + linked chunks]
    E --> H
    H --> I[LLM]
    I --> ANS[Answer]
```

Two stores: the graph holds structure, the vector store still holds chunks (so we can quote sources).

## Hybrid RAG

```mermaid
flowchart LR
    A[Documents] --> B[Chunk]
    B --> C[(Vector store)]
    B --> D[(BM25 index)]
    Q[Question] --> C
    Q --> D
    C --> E[Dense top-k]
    D --> F[Sparse top-k]
    E --> G[RRF fusion]
    F --> G
    G --> H[Cross-encoder rerank]
    H --> I[LLM]
    I --> ANS[Answer]
```

Single corpus, two views of it, fused then reranked.

## Agentic RAG

```mermaid
flowchart TD
    Q[Question] --> P[Planner LLM]
    P -->|need facts| T1[Tool: vector search]
    P -->|need entity links| T2[Tool: graph query]
    P -->|need fresh info| T3[Tool: web search]
    T1 --> R[Reflect / critique]
    T2 --> R
    T3 --> R
    R -->|enough?| ANS[Synthesize answer]
    R -->|no| P
```

A loop, not a pipeline. State accumulates across iterations.

## Shared components (`src/rag_compare/common/`)

- Chunker
- Embedding client
- LLM client
- Eval harness with golden Q&A set

Each pattern reuses these so differences are attributable to the *pattern*, not the plumbing.
