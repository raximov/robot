from __future__ import annotations

from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class TradingConfig:
    symbol: str = "XAUUSD"
    timeframe: str = "M15"
    bars: int = 1000
    risk_per_trade: float = 0.01
    max_daily_loss_pct: float = 0.03
    min_rr: float = 2.0
    atr_multiplier: float = 1.5
    max_spread_points: int = 40
    news_block_minutes: int = 30
    london_open_utc: time = time(7, 0)
    ny_close_utc: time = time(21, 0)


@dataclass(frozen=True)
class MT5Config:
    login: int | None = None
    password: str | None = None
    server: str | None = None
    path: str | None = None
    magic_number: int = 20260210
    deviation: int = 20


@dataclass(frozen=True)
class AppConfig:
    trading: TradingConfig = TradingConfig()
    mt5: MT5Config = MT5Config()


CONFIG = AppConfig()
