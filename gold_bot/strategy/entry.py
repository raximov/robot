from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class Signal:
    side: str
    reason: str


def build_signal(df: pd.DataFrame, patterns: pd.DataFrame) -> Signal | None:
    row = df.iloc[-1]
    p = patterns.iloc[-1]

    trend_up = row["ema_50"] > row["ema_200"]
    trend_down = row["ema_50"] < row["ema_200"]

    macd_line = row.get("MACD_12_26_9")
    macd_signal = row.get("MACDs_12_26_9")

    if trend_up and row["rsi_14"] < 45 and p["engulfing"] > 0 and macd_line > macd_signal:
        return Signal(side="buy", reason="trend+rsi pullback+bullish engulfing+macd")

    if trend_down and row["rsi_14"] > 55 and p["engulfing"] < 0 and macd_line < macd_signal:
        return Signal(side="sell", reason="trend+rsi pullback+bearish engulfing+macd")

    return None
