# Raspberry Pi Automated Trading Bot

Ein vollautomatisierter Trading Bot, der auf Raspberry Pi läuft. Der Bot führt Machine Learning-basierte Analysen durch und handelt automatisch an der Börse.

## Features

✅ **Vollautomatisiert**: Läuft 24/7 auf Raspberry Pi  
✅ **Machine Learning**: LSTM-basierte Vorhersagen  
✅ **Risikomangement**: Position Sizing, Stop Loss, Take Profit  
✅ **Paper Trading**: Sicheres Testen ohne echtes Geld  
✅ **Benachrichtigungen**: Email & Telegram Alerts  
✅ **Backtesting**: Strategie-Validierung  
✅ **Multi-Symbol**: Mehrere Aktien parallel  

## Projektstruktur

```
.
├── src/
│   ├── data_fetching.py           # Datenbeschaffung (Yahoo Finance)
│   ├── stock_analysis.py          # Basis-Analysen
│   ├── correlation_analysis.py    # Korrelationen
│   ├── risk_analysis.py           # Risikoanalyse
│   ├── monte_carlo_simulation.py  # Monte Carlo VaR
│   ├── lstm_prediction.py         # ML-Vorhersagen
│   ├── trading_engine.py          # Trade Execution (NEU)
│   ├── risk_manager.py            # Riskomanagement (NEU)
│   ├── notifier.py                # Benachrichtigungen (NEU)
│   └── backtest.py                # Backtesting (NEU)
├── pi_bot_main.py                 # Bot Hauptprogramm (NEU)
├── .env                           # Umgebungsvariablen (Konfiguration)
├── .env.example                   # Konfigurationsvorlage
├── RASPBERRY_PI_SETUP.md          # Setup-Anleitung (NEU)
├── requirements.txt               # Python Dependencies
└── README.md                       # Diese Datei
```

## Komponenten erklärt

### 1. **trading_engine.py** - Trade Execution
Führt echte Trades über Alpaca API aus:
- BUY/SELL Orders
- Position Management
- Order Tracking

### 2. **risk_manager.py** - Risikomangement
Verwaltet Risiken automatisch:
- Position Sizing basierend auf Risiko
- Stop Loss & Take Profit berechnen
- Maximum Exposure Control
- Drawdown Tracking

### 3. **notifier.py** - Benachrichtigungen
Sendet Alerts per:
- Email (Gmail)
- Telegram
- Multi-Channel Support

### 4. **pi_bot_main.py** - Orchestrierung
Hauptprogramm das läuft:
- Scheduled Analysis (täglich)
- Signal Generation
- Trade Execution
- Risk Monitoring
- 24/7 auf Raspberry Pi

### 5. **backtest.py** - Strategie-Validierung
Testet Strategie auf historischen Daten:
- Win Rate, Profit Factor
- Sharpe Ratio, Max Drawdown
- Trade Performance
- Risikokennzahlen

## Quick Start

### Installation

```bash
# Raspberry Pi vorbereiten (siehe RASPBERRY_PI_SETUP.md)
cd ~
git clone https://github.com/brittojo7n/BigDataProject...
cd BigDataProject-StockMarketTrendAnalysisAndPrediction
python3 -m venv trading_env
source trading_env/bin/activate
pip install -r requirements.txt
pip install alpaca-trade-api schedule
```

### Konfigurieren

```bash
# API Keys setzen
export ALPACA_API_KEY="your_key_here"
export ALPACA_SECRET_KEY="your_secret_here"

# Umgebungsvariablen bearbeiten
nano .env

# WICHTIG: PAPER_TRADING=true setzen!
```

### Starten

```bash
# Test-Lauf
python pi_bot_main.py

# Als Service (siehe Setup-Anleitung)
sudo systemctl start trading-bot
```

## Workflow

```
┌─────────────────────────────────┐
│   Tägliche Analyse (09:30)      │
│   - Daten laden                 │
│   - LSTM Vorhersagen            │
│   - Signale generieren          │
└──────────────┬──────────────────┘
               │
        ┌──────▼────────┐
        │  Signal OK?   │
        └──────┬───────┬┘
           Ja  │       │ Nein
              ▼        ▼
          ┌─────────┐ SKIP
          │ Trade   │
          │ möglich?│
          └──┬───┬──┘
           Ja│   │Nein
            ▼    ▼
        ┌──────────┐
        │ Position │
        │ öffnen   │
        └────┬─────┘
             │
    ┌────────▼────────┐
    │ Kontinuierliche  │
    │ Überwachung      │
    │ (Stop Loss/TP)   │
    └────────┬─────────┘
             │
    ┌────────▼────────┐
    │ Position        │
    │ schließen       │
    └─────────────────┘
```

## Beispiel Config

```yaml
trading:
  use_paper_trading: true      # Zuerst im Test-Modus
  symbols:
    - AAPL
    - GOOGL
    - MSFT
  min_confidence: 0.65         # Nur starke Signale

risk:
  account_balance: 100000      # Starting amount
  risk_per_trade: 0.02         # 2% = $2000
  max_positions: 5             # Max 5 offene Positionen
  stop_loss_pct: 0.05          # 5% Stop Loss
  take_profit_pct: 0.10        # 10% Take Profit

schedule:
  analysis_time: "09:30"       # US Market Open
  risk_check_interval: 60      # Jede Stunde
```

## Trading-Strategie

**Signal-Generierung:**
1. LSTM analysiert letzte 60 Tage
2. Vorhersagt nächste 180 Tage
3. Vergleicht mit aktueller Kurve
4. Generiert BUY/SELL Signal

**Position Management:**
- Position Size = Risk $ / Price Risk
- Risk = 2% pro Trade
- Stop Loss 5% unter Entry
- Take Profit 10% über Entry

**Exit-Strategien:**
- Stop Loss ausgelöst
- Take Profit erreicht
- Gegensignal

## Monitoring

```bash
# Bot Status
sudo systemctl status trading-bot

# Logs live
sudo journalctl -u trading-bot -f

# Trades ansehen
tail -f trading_bot.log | grep SELL

# Account Info
python -c "from src.trading_engine import TradingEngine; \
e=TradingEngine(); \
print(e.get_account_info())"
```

## Riskomanagement

⚠️ **KRITISCH: Vor echten Trades beachten!**

1. **Paper Trading Phase (3 Monate)**
   - Keine echten Trades
   - Echte Börsendaten
   - Alle Funktionen testen

2. **Micro Trading Phase (1 Monat)**
   - Nur $50-100 risikieren
   - Weiterhin alle Logs prüfen
   - Drawdown < 10% halten

3. **Skalieren (optional)**
   - Nur wenn konsistent profitabel
   - Langsam erhöhen
   - Tägliche Überwachung

## Backtesting

```python
from src.backtest import BacktestEngine
from src.data_fetching import get_closing_prices

# Daten laden
prices = get_closing_prices(['AAPL'])

# Backtest laufen
engine = BacktestEngine(initial_balance=100000)
results = engine.run_backtest('AAPL', prices, signals)

# Ergebnisse anschauen
engine.print_metrics(results)

# Exportieren
engine.export_results('backtest_results.csv')
```

## Wichtige Befehle auf Raspberry Pi

```bash
# Bot starten
sudo systemctl start trading-bot

# Bot stoppen
sudo systemctl stop trading-bot

# Neu starten
sudo systemctl restart trading-bot

# Logs anschauen
tail -100 logs/trading_bot.log

# Prozess prüfen
ps aux | grep pi_bot_main

# RAM-Nutzung
free -h

# Temperatur
vcgencmd measure_temp

# Disk-Speicher
df -h
```

## Fehlerbehebung

### API Connection Error
```bash
# API Keys prüfen
echo $ALPACA_API_KEY

# Internet testen
ping 8.8.8.8

# Alpaca Status: https://status.alpaca.markets
```

### Bot verbraucht zu viel RAM
```bash
# In .env:
LIGHTWEIGHT_MODE=true
CPU_ONLY=true

# Modell-Einstellungen:
LSTM_UNITS=10      # Reduzieren
LSTM_EPOCHS=1      # Reduzieren
```

### TensorFlow Error
```bash
pip uninstall tensorflow
pip install tensorflow-lite
```

## Performance-Tipps für Raspberry Pi

### Für Pi 4 (4GB):
- Alle Features aktiv
- Full LSTM Training möglich
- Multi-Symbol parallel

### Für Pi 3B+ (1GB):
- Lightweight Mode aktivieren
- Weniger Symbole
- Längere Check-Intervalle

### Für Pi Zero 2 (512MB):
- Sehr reduzierten Mode
- Max 1-2 Symbole
- Keine LSTM-Retraining
- Nur Kaufsignale

## Support & Community

- **Probleme**: GitHub Issues erstellen
- **Fragen**: Discussions forum
- **Docs**: RASPBERRY_PI_SETUP.md lesen
- **Logs**: trading_bot.log prüfen

## Sicherheit

🔒 **Wichtig:**
- NIEMALS API Keys hardcoden
- Umgebungsvariablen oder .env verwenden
- `.gitignore` beachten
- Paper Trading zuerst
- Daily Backup machen

## Lizenz

MIT License - Siehe LICENSE file

## Haftung

⚠️ **WICHTIG:** Dieses Programm ist für Bildungszwecke gedacht. Der Autor haftet nicht für finanzielle Verluste. Automatisiertes Trading ist riskant. Nutze immer Paper Trading zuerst!

---

**Version**: 1.0  
**Status**: Produktionsreife  
**Letzte Aktualisierung**: 2025-10-28

Viel Erfolg beim Trading! 🚀
