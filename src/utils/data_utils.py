import pandas as pd

def normalize_yfinance_df(df: pd.DataFrame,
                           symbol: str = ""
                           ) -> pd.DataFrame:
    """
    Normalizes a yfinance DataFrame to ensure
    that columns are simple strings (OHLCV)
    regardless of whether it has MultiIndex or not.
    """
    if df is None or df.empty:
        return df
    
    df = df.copy()
    
    # Case 1: MultiIndex in columns
    # ex: ("Close", "AAPL") → "Close"
    if isinstance(df.columns, pd.MultiIndex):
        # Flattens the MultiIndex taking the first level
        df.columns = [col[0] if isinstance(col, tuple)
                      else col
                      for col in df.columns]
        # Removes duplicate columns if any
        df = df.loc[:, ~df.columns.duplicated()]
    
    # Case 2: Columns with spaces or inconsistent
    # capitalization
    df.columns = [str(col).strip().capitalize()
                  if str(col).lower() in
                  ['open','high','low','close','volume',
                   'adj close']
                  else str(col)
                  for col in df.columns]
    
    # Ensures OHLCV columns as float
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )
    
    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(
            df["Volume"], errors="coerce"
        ).fillna(0)
    
    # Normalizes the index to DatetimeIndex without timezone
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    
    # Removes rows where Close is NaN
    if "Close" in df.columns:
        df = df.dropna(subset=["Close"])
    
    return df
