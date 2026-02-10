from __future__ import annotations


def calc_position_size(
    balance: float,
    risk_per_trade: float,
    stop_distance_price: float,
    tick_value: float,
    tick_size: float,
    min_lot: float,
    lot_step: float,
) -> float:
    if stop_distance_price <= 0 or tick_value <= 0 or tick_size <= 0:
        return 0.0

    risk_amount = balance * risk_per_trade
    stop_ticks = stop_distance_price / tick_size
    loss_per_lot = stop_ticks * tick_value
    raw_lot = risk_amount / loss_per_lot

    steps = int(raw_lot / lot_step)
    lot = max(min_lot, steps * lot_step)
    return round(lot, 2)


def reached_daily_loss_limit(day_pnl: float, balance_start_day: float, max_daily_loss_pct: float) -> bool:
    if balance_start_day <= 0:
        return True
    return day_pnl <= -(balance_start_day * max_daily_loss_pct)
