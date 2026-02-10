from __future__ import annotations

import logging
from typing import Any

import MetaTrader5 as mt5
import pandas as pd

from gold_bot.config.settings import MT5Config

LOGGER = logging.getLogger(__name__)


TIMEFRAME_MAP: dict[str, int] = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
}


class MT5Connector:
    def __init__(self, config: MT5Config) -> None:
        self.config = config

    def connect(self) -> None:
        if not mt5.initialize(path=self.config.path):
            raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")

        if self.config.login and self.config.password and self.config.server:
            ok = mt5.login(self.config.login, password=self.config.password, server=self.config.server)
            if not ok:
                raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

        LOGGER.info("Connected to MT5")

    def shutdown(self) -> None:
        mt5.shutdown()

    def get_rates(self, symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
        tf = TIMEFRAME_MAP[timeframe]
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
        if rates is None:
            raise RuntimeError(f"No rates returned for {symbol}")
        frame = pd.DataFrame(rates)
        frame["time"] = pd.to_datetime(frame["time"], unit="s", utc=True)
        return frame

    def symbol_info(self, symbol: str) -> Any:
        info = mt5.symbol_info(symbol)
        if info is None:
            raise RuntimeError(f"symbol_info not available for {symbol}")
        return info

    def tick(self, symbol: str) -> Any:
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise RuntimeError(f"tick not available for {symbol}")
        return tick
