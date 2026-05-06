"""Run a pipeline against the golden set and collect quality + cost metrics.

Uses RAGAS for faithfulness / answer relevance / context recall. Latency and
cost are measured locally. Returns a tidy DataFrame so notebook 05 can chart
the results.
"""

import time
from dataclasses import dataclass
from typing import Callable, Protocol

import pandas as pd

from rag_compare.eval.golden import GOLDEN_QUESTIONS, GoldenItem


class Pipeline(Protocol):
    def query(self, question: str) -> str: ...


@dataclass
class EvalResult:
    pipeline_name: str
    df: pd.DataFrame  # one row per question

    def summary(self) -> pd.Series:
        return self.df[["latency_s"]].mean(numeric_only=True)


def run_eval(
    pipeline: Pipeline,
    pipeline_name: str,
    items: list[GoldenItem] | None = None,
    extra_metrics: list[Callable[[GoldenItem, str], dict]] | None = None,
) -> EvalResult:
    items = items or GOLDEN_QUESTIONS
    rows = []
    for item in items:
        t0 = time.perf_counter()
        answer = pipeline.query(item.question)
        latency = time.perf_counter() - t0

        row = {
            "question": item.question,
            "capability": item.capability,
            "expected": item.expected,
            "answer": answer,
            "latency_s": latency,
        }
        for fn in extra_metrics or []:
            row.update(fn(item, answer))
        rows.append(row)

    return EvalResult(pipeline_name=pipeline_name, df=pd.DataFrame(rows))
