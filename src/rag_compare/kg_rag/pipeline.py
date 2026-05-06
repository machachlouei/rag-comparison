"""KG-RAG pipeline.

Build phase: extract (entity, relation, entity) triples from chunks with an LLM
and persist them in Neo4j. Keep the chunks themselves in a vector store so we
can quote sources alongside the graph traversal.

Query phase: link entities in the question to graph nodes, traverse the graph
to gather a relevant subgraph, and combine that with retrieved chunks for the
final answer.
"""

from dataclasses import dataclass

from llama_index.core import Document, PropertyGraphIndex, Settings, StorageContext
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

from rag_compare.common.config import get_settings
from rag_compare.common.embeddings import get_embedder
from rag_compare.common.llm import get_llm


@dataclass
class KGRagPipeline:
    index: PropertyGraphIndex

    @classmethod
    def build(cls, docs: list[Document]) -> "KGRagPipeline":
        cfg = get_settings()
        Settings.llm = get_llm()
        Settings.embed_model = get_embedder()

        graph_store = Neo4jPropertyGraphStore(
            username=cfg.neo4j_username,
            password=cfg.neo4j_password,
            url=cfg.neo4j_uri,
        )
        storage_context = StorageContext.from_defaults(property_graph_store=graph_store)

        extractor = SchemaLLMPathExtractor(llm=Settings.llm)

        index = PropertyGraphIndex.from_documents(
            docs,
            storage_context=storage_context,
            kg_extractors=[extractor],
            show_progress=True,
        )
        return cls(index=index)

    def query(self, question: str, top_k: int = 5) -> str:
        engine = self.index.as_query_engine(
            include_text=True,
            similarity_top_k=top_k,
        )
        return str(engine.query(question))
