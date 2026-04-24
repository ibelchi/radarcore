import pandas as pd
import numpy as np

class UniverseFilter:
    """
    Universal filter prior to any buy scan.
    Removes stocks not suitable due to lack of liquidity, history, market cap, or price recovery.

    SECTOR DIVERSIFICATION NOTE:
    Implement in the orchestrator: after filtering the entire universe, group by info_data['sector'],
    sort by score and cut to 25 per group.
    """

    def _check_zombie_criterion(self,
                                 hist_data: pd.DataFrame
                                 ) -> dict:
        """
        Returns {"passes": bool, "reason": str}
        
        A ticker is zombie if it has NO episodes of:
          - drawdown >= 20% from a local high
          - followed by a rebound >= 50% of that drawdown
          - occurring in the last 24 months (504 sessions)
        
        If it has this episode recently: PASS (valid swing)
        If it only has old episodes (>24m): ZOMBIE
        If it has no episodes: ZOMBIE
        """
        import numpy as np
        
        try:
            # Max window: last 5 years or all history
            max_window = min(252 * 5, len(hist_data))
            data = hist_data.tail(max_window).copy()
            
            # Recent window: last 24 months
            recent_window = min(504, len(data))
            
            passes_recent = False
            passes_old = False
            
            # Analyze rolling windows of 252 days
            window_size = 252
            step = 63  # every quarter
            
            for start in range(0, len(data) - window_size,
                               step):
                window = data.iloc[start:start + window_size]
                
                # High of the first half
                first_half = window.iloc[:126]
                max_price = first_half["High"].max()
                max_idx = first_half["High"].idxmax()
                
                # Low of the second half
                second_half = window.iloc[126:]
                min_price = second_half["Low"].min()
                min_idx = second_half["Low"].idxmin()
                
                if max_price <= 0:
                    continue
                    
                drawdown = (max_price - min_price) / max_price
                
                if drawdown < 0.20:
                    continue
                
                # Price at the end of the window
                end_price = window["Close"].iloc[-1]
                recovery_range = max_price - min_price
                
                if recovery_range <= 0:
                    continue
                    
                recovery = (end_price - min_price) / recovery_range
                
                if recovery >= 0.50:
                    # It's a valid episode — is it recent?
                    # Check if the low is within the last 24m
                    position_from_end = len(data) - (
                        data.index.get_loc(min_idx)
                        if min_idx in data.index
                        else len(data)
                    )
                    
                    if position_from_end <= 504:
                        passes_recent = True
                        break  # Found recent valid episode
                    else:
                        passes_old = True
            
            if passes_recent:
                return {
                    "passes": True,
                    "reason": "Recent swing recovery detected"
                }
            elif passes_old:
                return {
                    "passes": False,
                    "reason": "Zombie: only old recoveries (>24m ago)"
                }
            else:
                return {
                    "passes": False,
                    "reason": "Zombie: no swing recovery found"
                }
        
        except Exception as e:
            # In case of error, benefit of the doubt
            return {
                "passes": True,
                "reason": f"Zombie check skipped (error: {str(e)[:50]})"
            }

    def is_eligible(self, symbol: str, hist_data: pd.DataFrame, info_data: dict) -> dict:
        from src.utils.data_utils import normalize_yfinance_df
        hist_data = normalize_yfinance_df(hist_data)
        
        result = {
            "eligible": False,
            "reason": "",
            "passed_criteria": []
        }

        # Basic safety check
        if hist_data is None or hist_data.empty:
            result["reason"] = "Little or no historical data available"
            return result
        
        current_price = hist_data['Close'].iloc[-1]

        # 1. VOLUME
        try:
            vol_20d = hist_data['Volume'].tail(20).mean()
            if vol_20d >= 500_000 or (vol_20d * current_price) >= 20_000_000:
                result["passed_criteria"].append("Adequate volume and liquidity")
            else:
                result["reason"] = "Insufficient volume"
                return result
        except Exception as e:
            result["passed_criteria"].append(f"Volume (ignored by error: {e})")

        # 2. HISTORY
        try:
            # Minimum 6 months of data (much more permissive)
            if len(hist_data) < 126:
                result["reason"] = "Insufficient history (<6 months)"
                return result
            
            result["passed_criteria"].append("Sufficient history (>= 6 months)")
        except Exception as e:
            result["passed_criteria"].append(f"History (ignored by error: {e})")

        # 3. MARKET CAP
        try:
            mcap = info_data.get("market_cap", 0)
            if mcap >= 2_000_000_000:
                result["passed_criteria"].append("Market cap adequate")
            else:
                result["reason"] = "Insufficient market cap (<2B$)"
                return result
        except Exception as e:
            result["passed_criteria"].append(f"Market cap (ignored by error: {e})")

        # 4. MINIMUM PRICE
        try:
            if current_price > 5.0:
                result["passed_criteria"].append("Price > $5")
            else:
                result["reason"] = "Penny stock"
                return result
        except Exception as e:
            result["passed_criteria"].append(f"Minimum price (ignored by error: {e})")

        # 5. ZOMBIE CRITERION (Trazo key)
        zombie_check = self._check_zombie_criterion(hist_data)
        if not zombie_check["passes"]:
            result["reason"] = zombie_check["reason"]
            return result
        result["passed_criteria"].append("zombie_check")

        # 6. PRICE VS HISTORICAL ATH
        try:
            ath = hist_data['High'].max()
            if current_price >= ath * 0.10:
                result["passed_criteria"].append("Price vs ATH adequate")
            else:
                result["reason"] = "Price >90% below all-time high"
                return result
        except Exception as e:
            result["passed_criteria"].append(f"Price vs historical ATH (ignored by error: {e})")

        # If it passes all filters, it becomes eligible
        result["eligible"] = True
        return result
