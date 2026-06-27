from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from borsapy._providers.isyatirim import IsYatirimProvider
from borsapy.exceptions import DataNotAvailableError


def test_tries_ufrs_when_industrial_empty():
    p = IsYatirimProvider.__new__(IsYatirimProvider)
    p._cache_get = lambda k: None
    p._cache_set = lambda *a, **k: None
    p._MAX_PERIODS_PER_CALL = 5
    p._get_periods = lambda *a, **k: [2025]
    p._period_sort_key = lambda c: str(c)
    p.FINANCIAL_GROUP_INDUSTRIAL = "XI_29"
    p.FINANCIAL_GROUP_BANK = "UFRS"

    calls = []

    def fetch(**kwargs):
        calls.append(kwargs["financial_group"])
        if kwargs["financial_group"] == "UFRS":
            return pd.DataFrame({"2025": [1.0]}, index=["Satış Gelirleri"])
        return pd.DataFrame()

    p._fetch_financial_table = fetch
    p._resolve_last_n = lambda last_n, quarterly: 1

    df = IsYatirimProvider.get_financial_statements(
        p, "GARAN", "income_stmt", quarterly=True, financial_group=None, last_n=1
    )
    assert not df.empty
    assert "UFRS" in calls
    assert calls[0] == "XI_29"
