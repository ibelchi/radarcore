# RadarCore: Investment Guide (Concepts & Practice)

Welcome to **RadarCore**. This manual will help you understand how the **Buy the Recovery** strategy works and how you can use this software to learn about finance and swing trading from scratch.

---

## 1. What is the "Buy the Recovery" Strategy?

Historically, many people have heard the term "Buy the Dip". In RadarCore, we call it **Buy the Recovery** because it is more precise: we don't buy when the stock is actively crashing (a "falling knife"), but when it has already found a floor and has starting to recover.

The goal is to take advantage of the fact that the price tends to return to its average after a temporary setback.

---

## 2. Before Starting: Configuring the Scanner

When you configure the scanner, you see a series of parameters. Here is what they mean in plain language:

*   **Lookback Days**: This is how far back we look at the past to find the stock's highest price point. If you set 60 days, we look for the "Record" price of those 2 months to compare it with today's price.
*   **Min Drop %**: How much of a "discount" you want the stock to have before notifying you. If you set 15%, we only look for companies that have fallen at least 15% from their 60-day high.
*   **Min Rebound %**: This is the confirmation that we are no longer falling. If you set 2%, you want the stock to have already risen 2% from its lowest point.
*   **Symbol Limit**: How many companies in the market you want to analyze (0 to analyze them all, but it will take longer).

---

## 3. How is "Confidence" Calculated?

The confidence score (1-100%) you see for each opportunity is not black magic; it's the sum of scores according to four factors:

1.  **Drop Quality (30%)**: The closer the stock is to having fallen 40-50%, the more confidence the program has that there is a large return path.
2.  **Rebound Quality (20%)**: If the rebound is solid (between 5% and 10%), the program has more confidence that the recovery has already begun.
3.  **The Chart Pattern (25%)**:
    *   **L-BASE**: Wins the maximum confidence points. It means the price has stayed sideways, almost not moving for days. This suggests that big institutional investors are quietly "accumulating" the stock.
    *   **V-RECOVERY**: Wins fewer confidence points because it is a very fast and violent rise that tends to be more unstable.
4.  **Market Context (25%)**: If your stock has fallen for its own reasons while the entire market is rising (**Idiosyncratic Drop**), the program has more confidence in its solo recovery.

---

## 4. Key Financial Concepts

### Stop Loss (SL)
This is your **safety handbrake**. Imagine you buy a stock at $10. If suddenly the company continues to do poorly, the Stop Loss is an order that tells your bank: "If the stock drops back to $9, sell it immediately."
*   **What is it for?** Because if the company goes bankrupt, you will have only lost $1 (from 10 to 9), but you will have saved yourself from losing all $10. RadarCore marks this line in red on the charts.

### Targets (T1 and T2)
These are your "sell goals" where you collect profits.
*   **T1 (Conservative Target)**: Is a halfway recovery point (usually marked at 85% approximation to the previous high). This is where you might decide to sell half to lock in quick profits.
*   **T2 (Ideal Target)**: This is when the stock returns exactly to the peak price it had before falling. This is where the "Buy the Recovery" strategy is successfully completed.

### Reference Markets (The S&P 500 Case)
Even though you can scan the Spanish IBEX 35 or the German DAX, the program always uses the "American Market" (**SPY / S&P 500**) as a global reference. Why? Because if the American market falls hard, it is very difficult for any stock in any other market to rise healthily. It serves as a thermometer to know if your company's crash is an isolated case or if the whole world is in crisis.

---

## 5. Practical Case: Interpreting Charts

When you open a Plotly chart in RadarCore, look for these 3 colors:

1.  **The Red Zone**: This is the period when the stock was in free fall. The **Red Triangle** marks where it started (the high).
2.  **The Yellow Triangle**: This is the **Pivot**. The moment the fall stopped and the stock decided it wouldn't go any lower.
3.  **The Green Zone**: This is the recovery phase we are trying to take advantage of. Our goal is to move up from the yellow triangle towards the **Green Dashed Line (T2)**.

## Golden Rule: Diversification
Never put all your savings into a single stock, no matter how much "Confidence" the program has. The correct strategy involves having, for example, 10 different trades at the same time. This way, if one goes wrong and the **Stop Loss** is triggered, the other 9 can continue their course towards **T2** and give you an overall profit.
