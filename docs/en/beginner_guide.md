# RadarCore: Investment Guide (Concepts & Practice)

Welcome to **RadarCore**. This manual is designed to take you from a complete beginner to understanding how our virtual assistant works. We do not hide how the program works; we will teach you the underlying math, but doing so with real-world examples.

---

## 1. Fundamental Concepts
RadarCore does not predict the future. It utilizes a strategy called **Swing Trading** based on "Mean Reversion" (also known as Buy the Dip).

What does that mean? When a strong, healthy company drops abruptly in price due to generalized panic or a temporary bad news cycle, it tends to "rebound" until it recovers its real value.

### The Price Cycle
- **Peak / High**: The highest price a buyer has paid for a stock in recent months.
- **Bottom / Low / Pivot**: The floor. The exact moment everyone stops selling and the first people start buying back.
- **Breakout**: The moment the stock confirms it is genuinely rising.

---

## 2. How RadarCore Calculates an Opportunity (The Math)

RadarCore uses **three pillars** before recommending a stock to you. All mathematics are programmed in pure percentages so they automatically scale whether the stock is $10 or $1,000.

### Pillar A: The Real Drop (Drop %)
The program looks for discounts (sales). If a stock was at $100 and fell all the way to $80, it has dropped 20%.
> **Mathematical Formula**: `((Period High Price - Minimum Price) / Period High Price) * 100`

### Pillar B: Rebound Confirmation (Rebound %)
RadarCore *never* recommends buying while the stock is actively crashing (that is known as "catching a falling knife"). It waits to see that from the floor (Minimum), the stock has started going back up (a minimum of 2%).
> **Mathematical Formula**: `((Current Price - Minimum Price) / Minimum Price) * 100`

### Pillar C: The "Pattern" (The Chart's Shape)
RadarCore looks at the history of the price drop and classifies it:
* **L-BASE**: The stock dropped and has spent the last 10-15 days mostly moving sideways in a flat line. Mathematically: `Accumulated range < 8% over 10 days`. This usually means the big institutional funds (the rich) are quietly buying the stock back up ("accumulating"). THIS IS THE SAFEST PATTERN.
* **V-RECOVERY**: The stock falls and violently bounces right back. Mathematically: `Rebound > 5% very fast`. This is explosive but far more unstable to trade.

---

## 3. The Market Context: Systemic vs Idiosyncratic

RadarCore is smart, meaning it compares the drop of your single stock against the entire American Stock Market (The S&P 500 Index).

* **Market falls, Stock falls (Systemic)**: S&P 500 falls 10%, and your stock falls 12%. RadarCore subtracts it: `12% - 10% = 2% anomaly`. If it's below 5%, the App will tell you `"⚠️ Systemic Drop"`. Your company is likely completely fine, it's just the entire global market panicking. These take longer to recover.
* **Market rises, Stock falls (Idiosyncratic)**: The S&P 500 is going up, but your specific stock crashes. The App will tell you `"✅ Idiosyncratic Drop"`. This is the best situation! It means the stock can recover entirely on its own very fast because the rest of the world economy is doing fine.

The "Confidence" metric (1-100%) you see is calculated by summing points: The quality of the drop + Is it an L-BASE? + Is it an Idiosyncratic Drop?

---

## 4. Practical Case Step-By-Step

Imagine you are using RadarCore right now. What should you do?

1. **Scan (The Scanner)**: Click "Run Scanner". RadarCore reads the entire US market looking for "Buy the Dip" discounts.
2. **Read the Table (History)**: You see a company (ex: TSLA).
   - "Drop": 25% (It's a quarter cheaper!).
   - "Rebound": 4% (Perfect, the knife hit the floor and it's bouncing).
   - "Pattern": L-BASE (High safety).
3. **Check the Visual Chart**: Open it up. You'll see Target 1 (T1) outlined at 85% of the recovery height. That is your first major take-profit target.
4. **Protect Yourself (Stop Loss - SL)**: Look at the red dashed line at the bottom. If you buy the stock, log into your banking app and set an automatic "Stop Loss" so if the price hits that red line again, you sell automatically. You take a small 5% loss to save yourself from losing everything. **Never trade without a Stop Loss!**

## The Absolute Golden Rule for Beginners
It does not matter if a stock says "Confidence 99%". The CEO could get arrested tomorrow and the stock would plummet. Never invest all your money into 1 single RadarCore stock. Always divide it by 10 different companies. That is called **Diversifying your Risk**.
