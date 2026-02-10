from __future__ import annotations

import pandas as pd
import talib


def candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    open_ = df["open"].to_numpy()
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()
    close = df["close"].to_numpy()

    out["engulfing"] = talib.CDLENGULFING(open_, high, low, close)
    out["hammer"] = talib.CDLHAMMER(open_, high, low, close)
    out["shooting_star"] = talib.CDLSHOOTINGSTAR(open_, high, low, close)
    out["doji"] = talib.CDLDOJI(open_, high, low, close)
    return out
