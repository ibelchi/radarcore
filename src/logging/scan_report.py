from datetime import datetime
from src.logging.scan_logger import ScanLogger

def generate_scan_report(logger: ScanLogger) -> str:
    summary = logger.summary()
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    duration = summary.get("duration_seconds", 0)
    total = summary.get("total_analyzed", 0)
    found = summary.get("opportunities_found", 0)
    config = summary.get("config", {})

    # Specific counters based on skipping detail (UNIVERSE_FILTER)
    liq_count = 0
    market_count = 0
    zombie_count = 0
    
    for e in logger.events:
        if e["stage"] == "UNIVERSE_FILTER" and e["status"] == "SKIP":
            detail = e["detail"].lower()
            if "volume" in detail or "liquidity" in detail or "volum" in detail or "liquiditat" in detail:
                liq_count += 1
            if "market cap" in detail:
                market_count += 1
            if "zombie" in detail:
                zombie_count += 1

    report = f"""# RadarCore — Scan Report
**Date:** {date_str} | **Duration:** {duration}s

## Summary
- Tickers analyzed: {total}
- Opportunities found: {found}
- Discarded by liquidity: {liq_count}
- Discarded by market filter: {market_count}
- Discarded by zombie criterion: {zombie_count}

## Scan Configuration
- Universe: {config.get('universe', 'N/A')}
- Min drop: {config.get('min_drop_pct', 'N/A')}%
- Mode: {'Automatic' if config.get('auto_mode', True) else 'Watchlist'}

## Detected Opportunities
"""
    
    opportunities_found = False
    for e in logger.events:
        if e["stage"] == "STRATEGY" and e["status"] == "PASS":
            opportunities_found = True
            symbol = e["symbol"]
            detail = e["detail"]
            
            # Find bucket and score in subsequent events for the same symbol
            bucket = "N/A"
            score = "N/A"
            for sub_e in logger.events:
                if sub_e["symbol"] == symbol:
                    if sub_e["stage"] == "CLASSIFIER":
                        bucket = sub_e["detail"].replace("Bucket: ", "")
                    if sub_e["stage"] == "STRATEGY": # STRATEGY PASS detail usually contains opportunity info
                        # Try to extract score if present
                        pass

            report += f"### {symbol}\n"
            report += f"- Pattern: {bucket}\n"
            report += f"- {detail}\n\n"

    if not opportunities_found:
        report += "_No opportunities detected in this scan._\n"

    report += "\n## Discarded (summary by reason)\n"
    
    # Group by reason (detail) for SKIPs
    reasons = {}
    for e in logger.events:
        if e["status"] == "SKIP" or e["status"] == "FAIL":
            reason = e["detail"] or "Unknown"
            reasons[reason] = reasons.get(reason, 0) + 1
            
    # Top 5 reasons
    sorted_reasons = sorted(reasons.items(), key=lambda x: x[1], reverse=True)[:5]
    for reason, count in sorted_reasons:
        report += f"- {reason}: {count} tickers\n"

    return report
