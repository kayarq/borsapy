"""Contract tests for kayarq fork quote / statement semantics (mocked, no network)."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from borsapy.statements import extract_canonical_lines, match_row_label, REVENUE_LABELS
from borsapy.ticker import EnrichedInfo, FastInfo, Ticker


def test_revenue_label_match():
    labels = ["Sürdürülen Faaliyetler", "Satış Gelirleri", "BRÜT KAR (ZARAR)"]
    assert match_row_label(labels, REVENUE_LABELS) == "Satış Gelirleri"


def test_extract_canonical_lines():
    df = pd.DataFrame(
        {"2025Q2": [100.0, 10.0], "2025Q1": [90.0, 9.0]},
        index=["Satış Gelirleri", "DÖNEM KARI (ZARARI)"],
    )
    out = extract_canonical_lines(df, last_n_periods=2)
    assert "revenue" in out.index
    assert "net_income" in out.index
    assert out.loc["revenue", "2025Q2"] == 100.0


def test_yfinance_alias_previous_close_maps_to_prev_close():
    t = MagicMock()
    t._symbol = "GARAN"
    t._tradingview.get_quote.return_value = {
        "symbol": "GARAN",
        "last": 100.0,
        "prev_close": 99.0,
        "open": 99.5,
        "high": 101.0,
        "low": 98.0,
        "volume": 1,
    }
    info = EnrichedInfo(t)
    assert info["regularMarketPreviousClose"] == 99.0
    assert info["prev_close"] == 99.0


def test_fastinfo_previous_close_prefers_prev_close_not_close():
    t = MagicMock()
    t._symbol = "X"
    t.quote_snapshot.return_value = {
        "last": 100.0,
        "open": 99.0,
        "high": 101.0,
        "low": 98.0,
        "prev_close": 97.5,
        "volume": 10,
        "amount": None,
    }
    isy = MagicMock()
    isy.get_company_metrics.return_value = {"market_cap": 1e9, "pe_ratio": 5.0, "pb_ratio": 1.0}
    t._get_isyatirim.return_value = isy
    t.history.return_value = pd.DataFrame({"High": [1], "Low": [1], "Close": [1]})

    fi = FastInfo(t)
    assert fi.previous_close == 97.5
    assert fi.pe_ratio_source == "isyatirim"
