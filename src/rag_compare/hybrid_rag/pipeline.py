"""Hybrid RAG pipeline.

Dense retrieval (Qdrant + embeddings) and sparse retrieval (BM25) run in
parallel. Their results are fused with Reciprocal Rank Fusion, then a
cross-encoder reranks the top candidates before they reach the LLM.
"""

from dataclasses import dataclass

from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers.fusion_retriever import FUSION_MODES
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from rag_compare.common.chunking import chunk_documents
from rag_compare.common.config import get_settings
from rag_compare.common.embeddings import get_embedder
from rag_compare.common.llm import get_llm


@dataclass
class HybridRagPipeline:
    query_engine: RetrieverQueryEngine

    @classmethod
    def build(
        cls,
        docs: list[Document],
        collection: str = "rag_compare_hybrid",
        dense_top_k: int = 10,
        sparse_top_k: int = 10,
        rerank_top_n: int = 5,
    ) -> "HybridRagPipeline":
        cfg = get_settings()
        Settings.llm = get_llm()
        Settings.embed_model = get_embedder()

        nodes = chunk_documents(docs)

        client = QdrantClient(url=cfg.qdrant_url, api_key=cfg.qdrant_api_key)
        vector_store = QdrantVectorStore(client=client, collection_name=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

        dense = vector_index.as_retriever(similarity_top_k=dense_top_k)
        sparse = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=sparse_top_k)

        fusion = QueryFusionRetriever(
            retrievers=[dense, sparse],
            mode=FUSION_MODES.RECIPROCAL_RANK,
            similarity_top_k=dense_top_k + sparse_top_k,
            num_queries=1,  # set >1 to also generate query variants
            use_async=False,
        )

        reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-6-v2",
            top_n=rerank_top_n,
        )

        engine = RetrieverQueryEngine.from_args(
            retriever=fusion,
            node_postprocessors=[reranker],
        )
        return cls(query_engine=engine)

    def query(self, question: str) -> str:
        return str(self.query_engine.query(question))
