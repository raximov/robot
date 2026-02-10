from __future__ import annotations

import pandas as pd
import pandas_ta as ta


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["ema_50"] = ta.ema(data["close"], length=50)
    data["ema_200"] = ta.ema(data["close"], length=200)
    data["rsi_14"] = ta.rsi(data["close"], length=14)
    macd = ta.macd(data["close"], fast=12, slow=26, signal=9)
    data = data.join(macd)
    atr = ta.atr(data["high"], data["low"], data["close"], length=14)
    data["atr_14"] = atr
    return data.dropna().reset_index(drop=True)
