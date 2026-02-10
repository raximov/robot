from __future__ import annotations

import logging
from datetime import datetime, timezone

from gold_bot.config.settings import CONFIG
from gold_bot.core.execution import ExecutionEngine
from gold_bot.core.mt5_connector import MT5Connector
from gold_bot.core.risk import calc_position_size
from gold_bot.data.indicators import add_features
from gold_bot.strategy.entry import build_signal
from gold_bot.strategy.news_filter import NewsEvent, should_block_trading
from gold_bot.strategy.patterns import candlestick_patterns

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")
LOGGER = logging.getLogger("gold_bot")


def run_once() -> None:
    connector = MT5Connector(CONFIG.mt5)
    executor = ExecutionEngine(CONFIG.mt5)
    cfg = CONFIG.trading

    connector.connect()
    try:
        rates = connector.get_rates(cfg.symbol, cfg.timeframe, cfg.bars)
        feats = add_features(rates)
        pats = candlestick_patterns(feats)

        events: list[NewsEvent] = []
        if should_block_trading(events, cfg.news_block_minutes):
            LOGGER.info("News window active; skipping trade")
            return

        signal = build_signal(feats, pats)
        if signal is None:
            LOGGER.info("No signal")
            return

        info = connector.symbol_info(cfg.symbol)
        tick = connector.tick(cfg.symbol)
        spread_points = int((tick.ask - tick.bid) / info.point)
        if spread_points > cfg.max_spread_points:
            LOGGER.info("Spread too high (%s points)", spread_points)
            return

        atr = feats.iloc[-1]["atr_14"]
        is_buy = signal.side == "buy"
        entry = tick.ask if is_buy else tick.bid
        sl = entry - atr * cfg.atr_multiplier if is_buy else entry + atr * cfg.atr_multiplier
        tp = entry + atr * cfg.atr_multiplier * cfg.min_rr if is_buy else entry - atr * cfg.atr_multiplier * cfg.min_rr

        account = __import__("MetaTrader5").account_info()
        lot = calc_position_size(
            balance=account.balance,
            risk_per_trade=cfg.risk_per_trade,
            stop_distance_price=abs(entry - sl),
            tick_value=info.trade_tick_value,
            tick_size=info.trade_tick_size,
            min_lot=info.volume_min,
            lot_step=info.volume_step,
        )
        if lot <= 0:
            LOGGER.info("Lot size invalid, skip")
            return

        result = executor.send_market_order(cfg.symbol, lot, is_buy, sl, tp)
        LOGGER.info("Order sent: %s | reason=%s | lot=%.2f", result, signal.reason, lot)
    finally:
        connector.shutdown()


if __name__ == "__main__":
    LOGGER.info("Starting single-run cycle @ %s", datetime.now(timezone.utc).isoformat())
    run_once()
