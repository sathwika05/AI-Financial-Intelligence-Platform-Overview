# seeds

**Reference data and the frozen snapshot.** 50 tickers, a live seed that repopulates from real fundamentals, and a snapshot that freezes the database — including each chunk's embedding — so a benchmark score can only move because the code moved.

| | |
|---|---|
| `companies.csv` | the tickers |
| `seed_data.py` | the live seed |
| `snapshot.py` | create, restore and verify the frozen snapshot |
| `themes.py` | the sector and theme taxonomy |

_Implementations are private. This file lists what lives here and what it is responsible for._
