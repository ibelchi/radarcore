import yfinance as yf
from src.database.db import Opportunity
from src.utils.data_utils import normalize_yfinance_df

def backfill_rsi_and_vol(db):
    """
    For each opportunity that has rsi_14=None or vol_ratio_3m=None,
    reloads hist_data from yfinance and recalculates missing fields.
    """
    opportunities = db.query(Opportunity).all()
    
    # Filter in memory since SQLite JSON filtering can be tricky across versions
    to_update = []
    for op in opportunities:
        m = op.metrics or {}
        if m.get("rsi_14") is None or m.get("vol_ratio_3m") is None:
            to_update.append(op)
            
    if not to_update:
        return

    print(f"[backfill] Starting update for {len(to_update)} opportunities...")
    
    for op in to_update:
        try:
            print(f"[backfill] Processing {op.symbol}...")
            hist = yf.download(op.symbol, period="1y",
                               auto_adjust=True,
                               progress=False)
            hist = normalize_yfinance_df(hist, op.symbol)
            if hist.empty:
                continue
            
            m = op.metrics.copy() if op.metrics else {}
            
            # RSI
            if m.get("rsi_14") is None:
                delta = hist["Close"].diff()
                gain = delta.clip(lower=0).rolling(14).mean()
                loss = (-delta.clip(upper=0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                if not rsi.empty:
                    m["rsi_14"] = round(float(rsi.iloc[-1]), 1)
            
            # Vol ratio 3M
            if m.get("vol_ratio_3m") is None:
                vol_avui = float(hist["Volume"].iloc[-1])
                vol_mitja = float(hist["Volume"].tail(63).mean())
                m["vol_ratio_3m"] = round(
                    vol_avui / vol_mitja if vol_mitja > 0 else 1.0, 2
                )
            
            op.metrics = m
            db.commit()
        except Exception as e:
            print(f"[backfill] {op.symbol}: {e}")
            continue
    print("[backfill] Finished.")
