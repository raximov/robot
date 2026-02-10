# XAUUSD MT5 Auto Trading Bot (Skeleton)

Production-oriented skeleton for a full-auto **Gold (XAUUSD)** trading robot on **MT5**.

## Features included

- MT5 connector and execution engine
- Indicator pipeline (EMA, RSI, MACD, ATR)
- Candlestick pattern detection (TA-Lib)
- News-event trade blocking primitive
- Risk engine with position sizing
- Spread filter and ATR-based SL/TP

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add your MT5 credentials in `gold_bot/config/settings.py`.
3. Run one cycle:

```bash
python -m gold_bot.main
```

## Next steps

- Add real news source integration (ForexFactory/NewsAPI)
- Add continuous scheduler loop with session filters
- Add backtesting and walk-forward validation
- Persist trades/logs to PostgreSQL
- Add Telegram alerts and dashboard
