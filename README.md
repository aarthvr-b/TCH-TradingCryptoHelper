# 💹 TCH — Trading Crypto Helper

A **Textual-powered TUI** app to manage your crypto trades, calculate position size, and track performance.  
Built for traders who want a **lightweight**, **keyboard-driven**, and **risk-aware** workflow right from the terminal.

---

## 🚀 Features

- 📈 **Position Size Calculator**  
  Calculates how much to trade based on account size, risk %, entry, and stop loss.  

- ⚙️ **Leverage Suggestion**  
  Automatically recommends required leverage when your account balance is insufficient.

- 💰 **Trade Management**  
  Open, close, and delete trades — each stored persistently in a JSON log.

- 📊 **Interactive Trade History**  
  View all trades in a rich DataTable with PnL, notes, and easy navigation.

- 🧮 **PnL & Fee Calculation**  
  Automatically computes maker/taker fees and net profit/loss.

- 🧱 **Persistent Storage**  
  All trades are saved in `trades.json` (auto-created).

- 💬 **Popups & Confirmations**  
  Smart popup messages for validation, success/failure, and deletion confirmation.

- ⌨️ **Keyboard-Driven UX**  
  Navigate, confirm, and delete trades entirely from your keyboard.

---

## 🧰 Requirements

- Python 3.10+
- [Textual](https://textual.textualize.io/)
- [Rich](https://pypi.org/project/rich/)

Install dependencies:

```bash
pip install -r requirements.txt
```

Recommendend

```bash
python -m venv .venv
source .venv/bin/activate # macOS/Linux
# or
venv\Scripts\activate # Windows
```

---

## ▶️ Run the App

```bash
python tui.py
```

---

## 🧭 Navigation

| Action                 | Key / Button | Description                                               |
| ---------------------- | ------------ | --------------------------------------------------------- |
| **Open Trade**         | Menu option  | Enter pair, risk %, entry, stop, direction                |
| **Close Trade**        | Menu option  | Select an open trade, input exit price and optional notes |
| **View History**       | Menu option  | View all trades, including PnL and fees                   |
| **Toggle Delete Mode** | `D`          | Enable delete mode while in trade history                 |
| **Confirm Delete**     | `Y`          | Confirm deletion of selected trade                        |
| **Cancel Delete**      | `N`          | Cancel deletion                                           |
| **Back**               | `B`          | Return to previous screen                                 |
| **Exit**               | Menu option  | Quit the app                                              |

## 📁 File Structure

```bash
TCH-TradingCryptoHelper/
│── tui.py                      # Entry point for TUI app
│── core/
│   ├── trades.py               # Core trade logic (open/close/delete)
│   ├── calculator.py           # position sizing and computation 
│── storage.py                  # JSON read/write helpers
│── screens/
│   ├── main_menu_screen.py     # Main menu
│   ├── open_trade_screen.py    # Open trade UI
│   ├── close_trade_screen.py   # Close trade UI
│   ├── view_history_screen.py  # Trade history and delete mode
│   ├── popup_message.py        # Reusable popup message widget
│── trades.json                 # Saved trade data (auto-generated)
│── requirements.txt
│── README.md
│── .gitignore

```

---

## 🧮 Example Trade Flow

1. Open a Trade:

```yaml
Pair: BTCUSDT
Account size: 1000
Risk %: 2
Entry: 25000
Stop Loss: 24500
Direction: long
```

Popup shows:

```yaml
✅ Trade opened!

Pair: DOGEUSDT (LONG)
Quantity: 2246
Order Value: 548.58 USDT
Required Leverage: 1.49x
Risk per Trade: 19.50 USDT
```

2. Close the trade:

Enter:

```yaml
Exit price: 26000
Note: TP hit.
```

3. View trade history

| ID | Pair    | Dir  | Status | Entry | Exit  | Net Pnl | Notes  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  1  | BTCUSDT | LONG | CLOSED | 25000 | 26000 | 99.00   | Tp hit |

4. Delete Trades

- Press `D` to enable delete mode
- Select trade and press `Y` to confirm deletion

## 🧑‍💻 Author

Arthur J. Barbosa - AI Product Engineer & Trading Enthusiast
Building AI-driven tools for productivity and finance.
