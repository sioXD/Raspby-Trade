# 📈 Stock Market Trading Bot - Raspberry Pi

Vollautomatisierter Trading Bot für Aktienmarktanalyse und automatisierte Trades mit Machine Learning (LSTM), Risk Management und Telegram/Email Benachrichtigungen.

**Status:** ✅ Funktionsfähig auf Laptop und Raspberry Pi

---

## 🎯 Schnelleinstieg (3 Minuten)

### 1. Umgebungsvariablen einrichten

<https://app.alpaca.markets/user/profile#manage-accounts>

```bash
# Windows
.\setup_env.bat

# macOS/Linux
python setup_env.py
```

Der Script fragt nach deinen API Keys und speichert sie sicher in `.env`

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Bot testen

```bash
# Alle Tests ausführen
python test_bot_locally.py

# Interaktive Demos
python demo_bot.py

# Bot starten
python pi_bot_main.py
```

---

## 📚 Dokumentation

Alle Dokumentationen befinden sich im [`documentation/`](documentation/) Ordner:

### 🚀 **Erste Schritte**

- **[QUICK_START.md](documentation/QUICK_START.md)** - 3-Minuten Setup (Deutsch)
- **[SETUP_COMPLETE.md](documentation/SETUP_COMPLETE.md)** - Zusammenfassung des Setup-Prozesses

### 🔐 **Sicherheit & Konfiguration**

- **[ENV_SETUP.md](documentation/ENV_SETUP.md)** - Umgebungsvariablen detailliert (Deutsch)
- **[ENV_OVERVIEW.md](documentation/ENV_OVERVIEW.md)** - Übersicht der ENV-Variablen
- **[ENV_QUICKSTART.md](documentation/ENV_QUICKSTART.md)** - 2-Minuten ENV-Setup

### 💻 **Laptop Testing**

- **[LAPTOP_TESTING.md](documentation/LAPTOP_TESTING.md)** - Teste Bot auf Laptop vor Pi-Deployment

### 🔧 **Bot Features & Konfiguration**

- **[BOT_README.md](documentation/BOT_README.md)** - Bot Features und Workflow

### 🍓 **Raspberry Pi Deployment**

- **[RASPBERRY_PI_SETUP.md](documentation/RASPBERRY_PI_SETUP.md)** - Komplette Pi-Installation (45+ Schritte)

### 🏗️ **Code-Struktur**

- **[SRC_STRUCTURE.md](documentation/SRC_STRUCTURE.md)** - Detaillierte Beschreibung der src/-Ordnerstruktur und Module

---

## 🏗️ Projektstruktur

```
BigDataProject-StockMarketTrendAnalysisAndPrediction/
├── 📁 src/                              # Python Package (reorganisiert)
│   ├── 📁 analysis/                     # Datenanalyse Module
│   │   ├── data_fetching.py             # Yahoo Finance Daten
│   │   ├── stock_analysis.py            # Technische Analyse
│   │   ├── correlation_analysis.py      # Korrelationen
│   │   ├── risk_analysis.py             # Risiko-Metriken
│   │   └── monte_carlo_simulation.py    # Monte Carlo Simulationen
│   │
│   ├── 📁 ml/                           # Machine Learning Module
│   │   └── lstm_prediction.py           # LSTM Neural Network
│   │
│   ├── 📁 trading/                      # Trading & Risiko Module
│   │   ├── trading_engine.py            # Alpaca API Integration
│   │   ├── risk_manager.py              # Position Management
│   │   ├── backtest.py                  # Backtesting Engine
│   │   └── notifier.py                  # Email/Telegram Alerts
│   │
│   ├── 📁 utils/                        # Utility Module
│   │   └── main.py                      # Orchestration
│   │
│   └── env_loader.py                    # Sichere Konfiguration
│
├── 📁 documentation/                    # Alle Dokumentationen
│   ├── QUICK_START.md
│   ├── ENV_SETUP.md
│   ├── LAPTOP_TESTING.md
│   ├── BOT_README.md
│   ├── RASPBERRY_PI_SETUP.md
│   ├── SRC_STRUCTURE.md                 # NEU: Beschreibung der Module
│   └── ... weitere Docs
│
├── 📄 pi_bot_main.py                   # Bot Main Entry Point
├── 📄 demo_bot.py                      # Interaktive Demos
├── 📄 test_bot_locally.py              # Test Suite
├── 📄 .env                         # Environment Variables (NICHT in Git!)
├── 📄 .env.example                 # ENV Template
├── 📄 ENV_SETUP.md                 # Konfigurationsanleitung
├── 📄 setup_env.py                 # Interaktiver ENV Setup
├── 📄 setup_env.bat                # Windows ENV Setup
├── 📄 requirements.txt             # Python Dependencies
└── 📄 README.md                    # Dieses Dokument
```

---

## 🔧 Features

### 📊 **Datenanalyse**
- ✅ Historische Daten von Yahoo Finance
- ✅ Technische Indikatoren (Moving Averages, RSI, MACD, etc.)
- ✅ Korrelationsanalyse zwischen Aktien
- ✅ Value at Risk (VaR) Berechnung

### 🤖 **Machine Learning**
- ✅ LSTM Bi-Directional Neural Network
- ✅ Trend-Vorhersagen
- ✅ TensorFlow Graph-Mode Optimierung
- ✅ Retrain-fähig für Live-Daten

### 💰 **Trading Engine**
- ✅ Alpaca API Integration (Paper + Real)
- ✅ Automatische Order-Ausführung
- ✅ Position Tracking
- ✅ Mock Trading Mode (für Tests)

### 🛡️ **Risk Management**
- ✅ Position Sizing basierend auf Kelly Criterion
- ✅ Stop Loss / Take Profit Automatisierung
- ✅ Max Drawdown Limits
- ✅ Portfolio Value Limits

### 🔔 **Notifications**
- ✅ Email Alerts (Gmail mit 2FA)
- ✅ Telegram Bot Messages
- ✅ Trade Confirmations
- ✅ Risk Warnings

### 📈 **Backtesting**
- ✅ Historical Strategy Testing
- ✅ Sharpe Ratio / Profit Factor / Win Rate
- ✅ Multi-Symbol Testing
- ✅ CSV Export

### 🍓 **Raspberry Pi Optimiert**
- ✅ Lightweight Mode für Pi Zero/3
- ✅ CPU-Only (keine GPU)
- ✅ Systemd Service für 24/7 Operation
- ✅ Log Rotation
- ✅ Health Checks

---

## 📋 Workflow

```
┌─────────────────────────────────────────────────┐
│ 1. Konfiguration (setup_env.py)                 │
│    ↓                                             │
│ 2. Umgebungsvariablen (.env)                    │
│    ↓                                             │
│ 3. Daten laden (yfinance)                       │
│    ↓                                             │
│ 4. Technische Analyse                           │
│    ↓                                             │
│ 5. ML Vorhersage (LSTM)                         │
│    ↓                                             │
│ 6. Signal generieren                            │
│    ↓                                             │
│ 7. Risk Check (Risk Manager)                    │
│    ↓                                             │
│ 8. Trade ausführen (Alpaca API)                 │
│    ↓                                             │
│ 9. Notifications (Email/Telegram)               │
│    ↓                                             │
│ 10. Logging & Monitoring                        │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Verwendung

### Development (Laptop)

```bash
# Teste Bot lokal
python test_bot_locally.py

# Interaktive Demos
python demo_bot.py

# Starte Bot
python pi_bot_main.py
```

### Backtesting

```bash
# Teste Strategie auf historischen Daten
python backtest.py AAPL GOOGL MSFT 2020-01-01 2023-01-01
```

### Raspberry Pi

```bash
# Siehe RASPBERRY_PI_SETUP.md für Komplette Anleitung
ssh pi@raspberry
cd BigDataProject
systemctl start trading-bot
journalctl -u trading-bot -f  # Logs live anschauen
```

---

## 🔐 Sicherheit

### ✅ Best Practices

- `.env` Datei mit allen Secrets (nicht in Git!)
- API Keys via Umgebungsvariablen
- Gmail App Passwords (nicht echtes Passwort)
- Datei-Permissions 600 auf `.env`
- Keine Keys in Logs
- Paper Trading Standard (3+ Monate vor Real Trading)

### 🔒 Setup

1. Erstelle `.env` mit `setup_env.py`
2. Trage deine Alpaca Paper Trading Keys ein
3. (Optional) Email & Telegram Setup
4. Teste mit `test_bot_locally.py`
5. Starte Bot mit `python pi_bot_main.py`

---

## 📦 Dependencies

**Hauptabhängigkeiten:**
- Python 3.8+
- yfinance - Stock Data
- pandas/numpy - Data Processing
- TensorFlow/Keras - ML
- scikit-learn - ML Utilities
- alpaca-trade-api - Trading API
- python-dotenv - ENV Management
- schedule - Job Scheduling

Siehe `requirements.txt` für vollständige Liste mit Versions-Pins.

---

## 🧪 Testing

### Automatisierte Test Suite

```bash
python test_bot_locally.py
```

Tests:
- ✅ Data Fetching
- ✅ Stock Analysis
- ✅ Correlations
- ✅ Risk Management
- ✅ Trading Engine
- ✅ Notifications
- ✅ Backtesting
- ✅ Monte Carlo

### Interaktive Demos

```bash
python demo_bot.py
```

Demos:
- 📊 Trading Workflow
- 📈 Backtesting
- ⚠️ Risk Szenarien

---

## 📊 Konfiguration

Alle Konfigurationen erfolgen via `.env`-Datei (Umgebungsvariablen):

```bash
# Trading Konfiguration
TRADING_SYMBOLS=AAPL,GOOGL,MSFT,AMZN
PAPER_TRADING=true
MIN_CONFIDENCE=0.65
RISK_PER_TRADE=0.02

# Risk Management
MAX_PORTFOLIO_VALUE=100000
MAX_POSITIONS=5
STOP_LOSS_PCT=0.05
TAKE_PROFIT_PCT=0.10
MAX_DAILY_LOSS_PCT=0.10

# API Credentials
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
```

Siehe [ENV_SETUP.md](ENV_SETUP.md) für vollständige Dokumentation.

---

## 🤝 Git-Workflow

```bash
# Setup
git clone https://github.com/brittojo7n/BigDataProject-StockMarketTrendAnalysisAndPrediction.git
cd BigDataProject-StockMarketTrendAnalysisAndPrediction
pip install -r requirements.txt
python setup_env.py          # Erstelle .env

# Teste
python test_bot_locally.py

# Starte
python pi_bot_main.py
```

### ⚠️ Wichtig: `.env` nie committen!

```bash
# Prüfe ob .env in .gitignore
cat .gitignore | grep "\.env"

# Falls noch nicht: manuell .env löschen aus Git History
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 📞 Support & Troubleshooting

### Fehler: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Fehler: API Key nicht gefunden

```bash
# Prüfe ob .env existiert
ls -la .env

# Erstelle mit
python setup_env.py
```

### Fehler: Alpaca Connection

```bash
# Prüfe Internet
ping api.alpaca.markets

# Prüfe API Keys
python -c "from alpaca_trade_api import REST; REST('pk_test_...', 'sk_test_...').get_account()"
```

Siehe `documentation/` für spezifische Dokumentationen.

---

## 📈 Performance

### Laptop (Development)
- Datenladefähig: ~5 Aktien in ~2 Sekunden
- LSTM Training: ~30 Sekunden
- Vorhersage: ~500ms
- Test Suite: ~5-10 Minuten

### Raspberry Pi (Production)
- Lightweight Mode: CPU-Only
- ~15-20% CPU Auslastung
- ~200MB RAM Nutzung
- 24/7 Operation möglich

---

## 🎓 Lernquellen

- **Alpaca Trading API:** https://alpaca.markets
- **TensorFlow LSTM:** https://www.tensorflow.org/guide/keras/rnn
- **Technical Analysis:** https://en.wikipedia.org/wiki/Technical_analysis
- **Risk Management:** https://www.investopedia.com/terms/r/riskmanagement.asp

---

## 📄 License

Siehe `LICENSE` Datei

---

## 👨‍💻 Author

**brittojo7n** (GitHub)

---

## 🙏 Credits

- **yfinance** - Kostenlose Stock Data API
- **Alpaca** - Commission-free Broker API
- **TensorFlow** - Open Source ML Framework
- **pandas** - Data Manipulation Library

---

## 🚀 Nächste Schritte

1. **Jetzt lesen:** [`QUICK_START.md`](documentation/QUICK_START.md)
2. **Setup:** `python setup_env.py`
3. **Testen:** `python test_bot_locally.py`
4. **Deploy:** Siehe [`RASPBERRY_PI_SETUP.md`](documentation/RASPBERRY_PI_SETUP.md)

---

**Fragen? Siehe [`documentation/`](documentation/) für detaillierte Anleitungen!** 📖
