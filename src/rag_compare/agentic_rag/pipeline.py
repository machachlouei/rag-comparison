"""Agentic RAG pipeline.

A LangGraph state machine that decides which retriever to call (vector,
graph, or both), inspects results, optionally refines the query, and only
synthesizes an answer once it has enough evidence.

Tools are pluggable: this skeleton wires the hybrid retriever and the KG
retriever from this repo as agent tools, so the agent can compose patterns
the way production systems do.
"""

from dataclasses import dataclass
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from rag_compare.common.llm import get_llm
from rag_compare.hybrid_rag import HybridRagPipeline
from rag_compare.kg_rag import KGRagPipeline


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    question: str
    evidence: list[str]
    iterations: int


@dataclass
class AgenticRagPipeline:
    graph: object
    hybrid: HybridRagPipeline
    kg: KGRagPipeline | None
    max_iterations: int = 3

    @classmethod
    def build(
        cls,
        hybrid: HybridRagPipeline,
        kg: KGRagPipeline | None = None,
        max_iterations: int = 3,
    ) -> "AgenticRagPipeline":
        llm = get_llm()

        def plan(state: AgentState) -> AgentState:
            # Ask the LLM which tool to call given the question + evidence so far.
            # Implementation: see notebooks/03_agentic_rag_walkthrough.ipynb
            raise NotImplementedError("Plan node — implemented in notebook 03")

        def call_hybrid(state: AgentState) -> AgentState:
            answer = hybrid.query(state["question"])
            return {"evidence": state["evidence"] + [f"[hybrid] {answer}"]}

        def call_kg(state: AgentState) -> AgentState:
            if kg is None:
                return {"evidence": state["evidence"]}
            answer = kg.query(state["question"])
            return {"evidence": state["evidence"] + [f"[kg] {answer}"]}

        def reflect(state: AgentState) -> AgentState:
            # Decide: enough evidence? loop? or synthesize?
            raise NotImplementedError("Reflect node — implemented in notebook 03")

        def synthesize(state: AgentState) -> AgentState:
            raise NotImplementedError("Synthesize node — implemented in notebook 03")

        builder = StateGraph(AgentState)
        builder.add_node("plan", plan)
        builder.add_node("hybrid", call_hybrid)
        builder.add_node("kg", call_kg)
        builder.add_node("reflect", reflect)
        builder.add_node("synthesize", synthesize)
        builder.set_entry_point("plan")
        builder.add_edge("hybrid", "reflect")
        builder.add_edge("kg", "reflect")
        builder.add_edge("synthesize", END)

        return cls(graph=builder.compile(), hybrid=hybrid, kg=kg, max_iterations=max_iterations)

    def query(self, question: str) -> str:
        initial: AgentState = {
            "messages": [HumanMessage(content=question)],
            "question": question,
            "evidence": [],
            "iterations": 0,
        }
        result = self.graph.invoke(initial)
        return result["messages"][-1].content
