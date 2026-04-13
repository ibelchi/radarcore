# RadarCore: Technical Specification (Swing Trading Engine)

Documentation oriented towards financial analysts and quantitative algorithm designers.
RadarCore is an analysis terminal built around Mean Reversion algorithms within a **Buy the Recovery** framework.

---

## 1. Detection Algorithm: "Buy the Recovery"
The strategy orchestrated in the `src/strategies/buy_the_dip.py` module identifies trend inflection points following a bearish climax.

### Control Architecture (Configurable Parameters)
*   **Lookback Days**: Dynamic time window (N) for calculating the `MAX(High)` reference point.
*   **Min Drop %**: Significance filter for the relative drawdown: `(High - Low) / High`.
*   **Min Rebound %**: Impulse confirmation filter from the technical floor: `(Current - Low) / Low`.
*   **Liquidity Filters**: Requires `Market Cap > 10B` and `Volume > 1M` to ensure high-quality arbitrage potential.

---

## 2. Exit Definitions & Risk Management

*   **Stop Loss (SL)**: Indexed to the `Period_Low`. This is the point of technical invalidation for the mean-reversion setup.
*   **Target 1 (T1)**: Dynamic resistance set at 85% of the recovery path (`Period_High * 0.85`).
*   **Target 2 (T2)**: Classic return-to-the-mean goal (100% recovery of the previous record).

---

## 3. Pattern Recognition Engine

1.  **L-BASE**: Sideways accumulation profile.
    *   *Metric*: `(Max_10d - Min_10d) / Min_10d < 8%` & `Days_Since_Period_Low >= 10`.
2.  **V-RECOVERY**: Explosive rebound profile.
    *   *Metric*: `Rebound >= 5%` with expanded volatility range.

---

## 4. Relative Context (Systemic vs Idiosyncratic)

The system integrates a **Relative Momentum** calculation by comparing the asset's drop against the SPY benchmark (S&P 500) during the specific asset-drop window:
*   `Relative_Drop = Asset_Drop - SPY_Drop`.
*   If `Relative_Drop < 5%`: **Systemic**. Growing risk due to reliance on macro trends.
*   If `Relative_Drop >= 5%`: **Idiosyncratic**. Pure signal Alpha.

---

## 5. Confidence Score (Weighted Model)

The final score is a weighted model across four binary and scalar dimensions:
1.  **Drop Velocity** (30%): Scaled at `min(Drop_Pct / 40.0, 1.0)`.
2.  **Rebound Confirmation** (20%): Scaled at `min(Rebound_Pct / 10.0, 1.0)`.
3.  **Structural Strength** (25%): `L-BASE` grants 100% of this weight; `V-RECOVERY` grants 60%.
4.  **Market Alpha** (25%): Full bonus if the decline is confirmed as Idiosyncratic.
