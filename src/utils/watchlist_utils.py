from sqlalchemy.orm import Session
from src.database.db import Watchlist

def get_active_watchlist(db: Session) -> list:
    """Returns a list of active symbols in the watchlist."""
    records = db.query(Watchlist.symbol).filter(Watchlist.active == True).all()
    return [r[0] for r in records]

def should_deep_scan(symbol: str, db: Session, auto_mode: bool) -> bool:
    """
    If auto_mode is active, analyze everything.
    If inactive, only analyze if the symbol is in the active watchlist.
    """
    if auto_mode:
        return True
    
    exists = db.query(Watchlist).filter(
        Watchlist.symbol == symbol.upper(), 
        Watchlist.active == True
    ).first()
    return exists is not None

def add_to_watchlist(symbols: list, db: Session, source: str = 'auto') -> int:
    """
    Adds symbols to the watchlist ignoring duplicates.
    Returns the number of successfully added or reactivated items.
    """
    count = 0
    for sym in symbols:
        sym = str(sym).strip().upper()
        if not sym:
            continue
            
        existing = db.query(Watchlist).filter(Watchlist.symbol == sym).first()
        
        if existing:
            if not existing.active:
                existing.active = True
                existing.source = source
                count += 1
        else:
            new_item = Watchlist(symbol=sym, source=source, active=True)
            db.add(new_item)
            count += 1
            
    db.commit()
    return count
