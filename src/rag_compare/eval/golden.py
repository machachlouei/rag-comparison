"""Golden Q&A set tied to the starter Wikipedia corpus (AI labs / LLMs).

Each item targets a different *capability* so the side-by-side comparison
reveals where each pattern shines:

- single_hop:   one fact, one document          (baseline territory)
- multi_hop:    join facts across documents     (KG-RAG / Agentic shine)
- exact_term:   precise version / paper / date  (Hybrid / BM25 wins)
- aggregation:  list / count across documents   (Agentic shines)
- unanswerable: not in corpus                   (faithfulness check)

Expected answers are short canonical forms — pipelines may phrase differently.
The eval harness should compare semantically (LLM-as-judge or RAGAS).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GoldenItem:
    question: str
    expected: str
    capability: str  # single_hop | multi_hop | exact_term | aggregation | unanswerable


GOLDEN_QUESTIONS: list[GoldenItem] = [
    # --- single_hop -------------------------------------------------------
    GoldenItem(
        question="Who is the CEO of OpenAI?",
        expected="Sam Altman",
        capability="single_hop",
    ),
    GoldenItem(
        question="What company makes the Claude language model?",
        expected="Anthropic",
        capability="single_hop",
    ),
    GoldenItem(
        question="Which lab developed the Gemini model?",
        expected="Google DeepMind",
        capability="single_hop",
    ),

    # --- multi_hop --------------------------------------------------------
    GoldenItem(
        question=(
            "Which AI lab was founded by former OpenAI employees and develops the Claude model?"
        ),
        expected="Anthropic",
        capability="multi_hop",
    ),
    GoldenItem(
        question=(
            "Who co-founded the lab behind Claude, and what role did they "
            "previously hold at OpenAI?"
        ),
        expected="Dario Amodei (and Daniela Amodei); Dario was VP of Research at OpenAI.",
        capability="multi_hop",
    ),
    GoldenItem(
        question=(
            "Which deep learning architecture, introduced in a 2017 Google paper, "
            "underlies GPT-4, Claude, and Gemini?"
        ),
        expected="The Transformer (introduced in 'Attention Is All You Need').",
        capability="multi_hop",
    ),

    # --- exact_term -------------------------------------------------------
    GoldenItem(
        question=(
            "What is the exact title of the 2017 paper that introduced "
            "the Transformer architecture?"
        ),
        expected="Attention Is All You Need",
        capability="exact_term",
    ),
    GoldenItem(
        question="What does the acronym RLHF stand for?",
        expected="Reinforcement Learning from Human Feedback",
        capability="exact_term",
    ),
    GoldenItem(
        question="In what year was Anthropic founded?",
        expected="2021",
        capability="exact_term",
    ),

    # --- aggregation ------------------------------------------------------
    GoldenItem(
        question=(
            "List the major AI labs covered in the corpus that have released "
            "a flagship large language model."
        ),
        expected=(
            "OpenAI (GPT-4), Anthropic (Claude), Google DeepMind (Gemini), "
            "Meta (Llama), Mistral AI."
        ),
        capability="aggregation",
    ),

    # --- unanswerable -----------------------------------------------------
    GoldenItem(
        question="What was OpenAI's revenue in fiscal year 2030?",
        expected="I don't know based on the provided sources.",
        capability="unanswerable",
    ),
]
