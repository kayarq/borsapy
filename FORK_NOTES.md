# kayarq/borsapy (fork of saidsurucu/borsapy)

**Version:** 0.10.3+kayarq.1  
**Local:** `/home/kaya/borsapy`  
**Paired MCP:** `/home/kaya/borsa-mcp` pins this tree (editable / path dependency).

## Implemented on this fork

1. **Quote contract** — `FastInfo.previous_close` uses `prev_close` (then history[-2]), not ambiguous `close`.
2. **yfinance aliases** — `regularMarketPreviousClose` → `prev_close`.
3. **Basic keys** — explicit `prev_close` on quote dict path.
4. **UFRS fallback** — `IsYatirimProvider.get_financial_statements` tries XI_29 then UFRS when group unset (banks).
5. **`Ticker.quote_snapshot()`** — TV-only cheap quote (no 1y hist / metrics).
6. **`Ticker.get_income_stmt_canonical()`** + `borsapy.statements` — revenue / net_income extraction.
7. **Metrics source tags** — `pe_ratio_source` / `pb_ratio_source` on FastInfo.

## Stack

```text
Grok / agents
    → kayarq/borsa-mcp (assurance + MCP tools)
        → kayarq/borsapy (this package)
            → TradingView / İş Yatırım / KAP / …
```
