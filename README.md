# TCH - Trading Crypto Helper

A python-based crypto trading helper tool for position sizing, leverage calculation and trade tracking.
Designed for traders who want a **simple, reliable, and version-controlled** workflow for managing their trades.

---

## Features

- Calculate **position size** based on account size, risk percentage, entry, and stop loss.
- Automatically suggest **leverage** if you capital is insufficient.
- Track **long and short trades**.
- Log **entry, exit, PnL, fees, and notes** for each trade.
- Store trade history in **JSON** format.
- Color-coded trade history in the terminal using **Rich**.
- Confirmation step to **avoid input mistakes** before opening a trade.
- Easy to extend with **TUI / GUI** in the future.

--- 

## Requirements

- Python 3.10+
- [Rich](https://pypi.org/project/rich/) (`pip install rich`)

Optional: use a virtual environment to isolate dependencies.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/aarthvr-b/TCH-TradingCryptoHelper.git
cd TCH-TradingCryptoHelper
```
2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate #macOs/Linus
venv\Scripts\activate     #Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main program:

```bash
python main.py
```

## Menu Options

1. **Open Trade** - Input pair, entry, stop loss, risk %, and direction (long/short). Confirm before saving.
2. **Close Trade** - Select a trade, input exit price and optional notes. PnL and fees are calculated automatically.
3. **View History** - Shows a table of all trades with color-coded PnL.
4. **Exit** - Quit the program 

---

## File Structure

```bash
TCH-TradingCryptoHelper/
│── calculator.py      # Position sizing and fee calculations
│── trades.py          # CLI trade management
│── storage.py         # JSON storage handling
│── main.py            # Entry point
│── trades.json        # Trade history (auto-generated)
│── requirements.txt   # Dependencies
│── README.md
│── .gitignore
```

---

## Example Trade Flow

1. Open a Trade: 
```yaml
Pair: BTCUSDT
Account size: 1000
Risk %: 2
Entry: 25000
Stop Loss: 24500
Direction: long
```
2. Confirm the trade.
3. Close the trade:
```yaml
Exit price: 26000
Note: TP hit.
```
4. View trade history

ID | Pair    | Dir  | Status | Entry | Exit  | Net Pnl | Notes  
--- | --- | --- | --- | --- | --- | --- | ---
 1  | BTCUSDT | LONG | CLOSED | 25000 | 26000 | 99.00   | Tp hit 
