def is_not_recommended_today(metrics: dict) -> tuple[bool, str]:
    """
    Returns (True, reason) if entry is not recommended today based on technical metrics.
    """
    rsi = metrics.get("rsi_14", 0) or 0
    phase = metrics.get("phase", "")
    days_to_earnings = metrics.get("days_to_next_earnings")
    
    if rsi >= 75:
        return True, f"Overbought RSI ({rsi:.0f})"
    if phase == "LATE":
        return True, "LATE phase — low upside"
    if days_to_earnings is not None and days_to_earnings <= 7:
        return True, f"Earnings in {days_to_earnings} days"
    return False, ""
