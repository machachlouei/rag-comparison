# Data

`raw/` is where you put source documents. Anything `SimpleDirectoryReader` understands works: `.pdf`, `.md`, `.txt`, `.html`, `.docx`.

`processed/` holds derived artifacts (chunks, extracted triples, embeddings caches). Gitignored.

## Suggested starter corpora

| Use case | Source | Size |
|---|---|---|
| Biomedical QA | PubMed abstracts via `pubmed_parser` | 50–200 abstracts |
| Financial | SEC EDGAR 10-K filings (one company) | 1–3 filings |
| General | Wikipedia articles via `wikipedia` lib | 20–50 articles |

Pick a domain with **named entities** and **relationships between them** — that's where KG-RAG actually shines and the comparison gets interesting.

## License

Document any redistribution constraints for whatever corpus you use here.
