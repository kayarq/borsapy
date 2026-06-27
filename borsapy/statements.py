"""Canonical statement line helpers (kayarq fork).

İş Yatırım returns Turkish IFRS labels. Map common rows to stable IDs for agents/MCP.
"""
from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

REVENUE_LABELS = (
    "satış gelirleri",
    "satis gelirleri",
    "hasılat",
    "hasilat",
    "total revenue",
    "revenue",
    "net sales",
)
NET_INCOME_LABELS = (
    "dönem karı (zararı)",
    "donem kari (zarari)",
    "dönem kari (zarari)",  # ascii-folded İ
    "donem karı (zararı)",
    "dönem karı/zararı",
    "dönem kari/zarari",
    "sürdürülen faaliyetler dönem karı/zararı",
    "dönem net karı (zararı)",
    "net income",
    "net kar",
)

_EXCLUDE_NI = (
    "durdurulan",
    "vergi öncesi",
    "vergi oncesi",
    "dağılımı",
    "dagilimi",
    "brüt kar",
    "brut kar",
)


def match_row_label(
    index_labels: Iterable[str],
    candidates: tuple[str, ...],
    *,
    exclude_substrings: tuple[str, ...] = (),
) -> Optional[str]:
    lowered = [(str(lab), str(lab).lower().strip()) for lab in index_labels]

    def excluded(low: str) -> bool:
        return any(ex in low for ex in exclude_substrings)

    for cand in candidates:
        c = cand.lower().strip()
        for orig, low in lowered:
            if excluded(low):
                continue
            if low == c:
                return orig
    hits: list[tuple[int, str]] = []
    for cand in candidates:
        c = cand.lower().strip()
        for orig, low in lowered:
            if excluded(low):
                continue
            if c in low:
                hits.append((len(low), orig))
    if hits:
        hits.sort(key=lambda x: x[0])
        return hits[0][1]
    return None


def extract_canonical_lines(
    df: pd.DataFrame,
    *,
    last_n_periods: int | None = 4,
) -> pd.DataFrame:
    """Return a small DataFrame with rows revenue / net_income and period columns."""
    if df is None or df.empty:
        return pd.DataFrame()
    cols = list(df.columns)
    if last_n_periods is not None:
        cols = cols[:last_n_periods]
    labels = [str(i) for i in df.index]
    rev = match_row_label(labels, REVENUE_LABELS)
    ni = match_row_label(labels, NET_INCOME_LABELS, exclude_substrings=_EXCLUDE_NI)
    rows = {}
    if rev is not None:
        rows["revenue"] = [df.loc[rev, c] for c in cols]
    if ni is not None:
        rows["net_income"] = [df.loc[ni, c] for c in cols]
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows, index=cols).T
    out.index.name = "line_item"
    return out
