import pandas as pd
from src.strategies.bucket_scorers.base_scorer import BaseBucketScorer

class LateralScorer(BaseBucketScorer):
    def score(self, hist_data: pd.DataFrame, metrics: dict) -> dict:
        total_score = 0
        
        high_15d = hist_data['High'].tail(15).max()
        low_15d = hist_data['Low'].tail(15).min()
        range_15d = (high_15d - low_15d) / low_15d * 100 if low_15d > 0 else 0
        
        if range_15d < 5:
            total_score += 40
        elif range_15d < 8:
            total_score += 20
            
        # Lateral days estimation (approximate by how long it's been without breaking the channel)
        # We use the history up to where the range was below 10%
        # This is complex, we calculate simply as the number of days since the price is contained
        lateral_days = 15 # Minimum the 15 from above if exceeded
        try:
            for i in range(16, min(60, len(hist_data))):
                h = hist_data['High'].tail(i).max()
                l = hist_data['Low'].tail(i).min()
                r = (h - l) / l * 100
                if r < 10:
                    lateral_days = i
                else:
                    break
        except:
            pass
            
        if lateral_days >= 20:
            total_score += 30
            
        vol_5d = hist_data['Volume'].tail(5).mean()
        vol_20d = hist_data['Volume'].tail(20).mean()
        vol_decreasing = vol_5d < vol_20d
        
        if vol_decreasing:
            total_score += 30
            
        vol_str = "decreasing" if vol_decreasing else "stable"
        reasoning = f"Lateral base {lateral_days}d, range {range_15d:.1f}%, volume {vol_str}"
        
        return {
            "score": min(100, total_score),
            "reasoning": reasoning,
            "key_metrics": {
                "lateral_days": lateral_days,
                "range_pct": range_15d,
                "volume_trend": "decreasing" if vol_decreasing else "increasing"
            }
        }
