# RadarCore: Technical Specification (Swing Trading Engine)

Documentation oriented towards financial analysts and quantitative algorithm designers.
RadarCore is an analysis terminal built around Mean Reversion algorithms specifically crafted for the Swing Trading ecosystem.

---

## 1. Detection Algorithm: "Buy The Dip"
The core evaluation matrix is located in the `src/strategies/buy_the_dip.py` module. It does not look for historical absolute minimums; instead, it looks for mean regressions within short-term volatility windows.

### Initial Parametric Architecture
*   `lookback_days` = 60 days (Context window to identify the asset's latest climax).
*   `min_drop_pct` = 15.0% (Significance threshold to consider the price stressed).
*   `min_rebound_pct` = 2.0% (Technical confirmation of trend reversal).

The algorithm processes price arrays with an upfront liquidity filter to cut through "penny stock" noise (requires `min_market_cap_b` > 10 and volume > 1M).

---

## 2. Technical Evaluation Formalization

Unlike vanilla screeners, RadarCore corrects "Drop" appreciation by indexing reading closures purely against the local technical minimum, rather than the real-time tick.

*   **Real Relative Drop**:
    ```
    Drop_From_High (%) = ((Period_High - Period_Low) / Period_High) * 100
    ```
    *(This mitigates the risk of discarding consolidated technical models suffering from midnight gap-ups).*

*   **Friction Point (Rebound)**:
    ```
    Rebound (%) = ((Current_Price - Period_Low) / Period_Low) * 100
    ```

---

## 3. Typology (Pattern Recognition Engine)

The architecture analyses micro-cycles (10-15 day windows) post the recent extreme, searching for divergence among underlying directional volumes:

1.  **L-BASE**: Consolidation profile. Defines institutional accumulation zones where the descending impact (Bear Trend) has exhausted itself against a wall of stagnant liquidity (sideways).
    *   *Rules*: `(Max_price_10d - Min_price_10d) / Min_price_10d < 8%` and `Days_Since_Period_Low >= 10`.
2.  **V-RECOVERY**: Classic *Snap-back* indicating highly emotional stress where supply immediately extinguishes against massive market buys.
    *   *Rules*: `Rebound >= 5%` with implicit high baseline variance.

---

## 4. Relative Contextualization (The Systemic Filter)

An aggressive drop beneath a "Macro-Bear" framework lacks Beta-adjusted attraction. Therefore, RadarCore orchestrates a parallel SPY downloader (representing Beta=1 Market Risk) with "Zero-Retention".

Differential Calculation:
```
Relative_Drop_Pct  = (Drop_From_High_Pct_{Asset}) - (Drop_Pct_{SPY})
```
*   If `Relative_Drop_Pct < 5.0%` = **Systemic**. The broader market drags the asset. The arbitrage operator must approach with alert.
*   If `Relative_Drop_Pct >= 5.0%` = **Idiosyncratic**. Pure potential Alpha for Swing trading.

---

## 5. Confidence Score (Evaluation Model)

The RadarCore opportunity rubric (`0-100%`) is synthetically calibrated across 4 dimensions for the setup:

1.  **Mass Drop** (30% MAX): Free scale weight at `min(Drop_Pct / 40.0, 1.0)`.
2.  **Rebound Validation** (20% MAX): Active impulse validation: `min(Rebound_Pct / 10.0, 1.0)`.
3.  **Pattern Architecture** (25% MAX): Risk-yield assignment favors `L-BASE (25%)` over `V-RECOVERY (15%)` based on commercial breakout survival rates.
4.  **Market Decoupling** (25% MAX): Outputs Alpha if the model proves a `is_systemic == False` decline to avoid indexation trapping for the directional operator.

The chart (procedurally generated via Plotly, adding zero I/O weight to Streamlit overhead) overlays via pre-computed vectors offering crisp guidance such as Target 1 `T_1=Period_high * 0.85`.
