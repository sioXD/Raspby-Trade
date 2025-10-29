# Trading Bot auf Laptop testen - Schnellstart

## 🚀 3-Minuten Setup

### Windows
```batch
run_tests.bat
```

### macOS/Linux
```bash
bash run_tests.sh
```

Das Script macht automatisch:
1. ✓ Python Prüfung
2. ✓ Dependencies installieren
3. ✓ Virtual Environment erstellen
4. ✓ Test Suite ausführen
5. ✓ Demo-Optionen anzeigen

---

## 📊 Manuelle Installation (wenn Scripts nicht funktionieren)

### Schritt 1: Python Vorbereitung

```bash
# Python-Version prüfen (muss 3.8+ sein)
python --version

# Virtual Environment erstellen
python -m venv trading_env

# Aktivieren:
# Windows:
trading_env\Scripts\activate.bat
# macOS/Linux:
source trading_env/bin/activate
```

### Schritt 2: Dependencies

```bash
pip install -r requirements.txt
```

**Falls Fehler:** Probiere einzeln:
```bash
pip install yfinance
pip install pandas
pip install numpy
pip install scikit-learn
pip install tensorflow
pip install alpaca-trade-api
```

### Schritt 3: Test Suite starten

```bash
python test_bot_locally.py
```

---

## 🎮 Interaktive Demos ausführen

Nach erfolgreichem Test:

```bash
# Interaktives Menü
python demo_bot.py

# Oder direkt eine Demo:
python demo_bot.py workflow      # Trading Workflow
python demo_bot.py backtest      # Backtesting
python demo_bot.py risk          # Risk Szenarien
```

---

## 📈 Was wird getestet?

```
TEST SUITE - 8 Tests
├── TEST 1: Data Fetching           ← Yahoo Finance API
├── TEST 2: Stock Analysis          ← Moving Averages, Returns
├── TEST 3: Correlations            ← Abhängigkeiten zwischen Aktien
├── TEST 4: Risk Management         ← Position Sizing, Stop Loss
├── TEST 5: Trading Engine          ← Mock Orders (KEIN echtes Geld!)
├── TEST 6: Notifier                ← Email/Telegram Setup
├── TEST 7: Backtesting             ← Strategie testen
└── TEST 8: Monte Carlo             ← Risiko-Simulation
```

**Ergebnis:** Entweder `✓ PASS` oder `✗ FAIL` pro Test

---

## 🎯 Test-Szenarien

### Szenario 1: Nur testen ob alles funktioniert
```bash
python test_bot_locally.py
# Dauer: 5-10 Minuten
# Ergebnis: Pass/Fail Report
```

### Szenario 2: Bot-Workflow verstehen
```bash
python demo_bot.py workflow
# Sieht wie ein echter Handelstag aus
# Zeigt Position Sizing, Stop Loss, Take Profit
```

### Szenario 3: Strategie backtesten
```bash
python demo_bot.py backtest
# Testet Simple Moving Average Strategie
# Zeigt Profitabilität, Sharpe Ratio, Drawdown
```

### Szenario 4: Risk Management verstehen
```bash
python demo_bot.py risk
# 4 verschiedene Risk-Szenarien
# Zeigt wie Stop Loss, Max Positions funktionieren
```

---

## ⚡ Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'yfinance'"

```bash
pip install yfinance
# Oder alle Dependencies neu:
pip install -r requirements.txt --force-reinstall
```

### Problem: "ConnectionError: API Connection Failed"

```
- Internetverbindung prüfen
- Yahoo Finance API erreichbar?
- Firewall/Proxy blockiert?
→ Später nochmal versuchen
```

### Problem: "TensorFlow OutOfMemory"

```bash
# Leichtgewichtige Version:
pip uninstall tensorflow
pip install tensorflow-lite

# Oder in .env:
# Reduziere LSTM Größe: LSTM_UNITS=10, LSTM_EPOCHS=1
```

### Problem: Scripts starten nicht

```bash
# Explizit Python aufrufen:
python test_bot_locally.py
python demo_bot.py

# Mit vollständigem Pfad:
/usr/bin/python3 test_bot_locally.py

# Berechtigungen prüfen (Linux/Mac):
chmod +x run_tests.sh
./run_tests.sh
```

---

## 📝 Test Outputs verstehen

### Test 1 Output: DATA FETCHING
```
✓ Erfolgreich! 1260 Datenpunkte geladen
Shape: (1260, 3)

Letzte 5 Tage:
            AAPL    GOOGL    MSFT
2024-10-24 195.50 140.25  380.00
2024-10-25 197.30 141.50  381.75
```
✅ **OK:** Yahoo Finance funktioniert

### Test 4 Output: RISK MANAGEMENT
```
Position Size: 267 shares (Risk: $2,000.00)
Stop Loss: $142.50 (5%)
Take Profit: $165.00 (10%)
Trade Valid: True
```
✅ **OK:** Risk Manager funktioniert

### Test 7 Output: BACKTESTING
```
Total Trades:        42
Winning Trades:      28 (66.67%)
Total Return:        8.45%
Sharpe Ratio:        1.24
Max Drawdown:        -8.50%
```
✅ **OK:** Strategie ist profitabel!

---

## 🎓 Nach dem Test

### ✓ Alles erfolgreich?
```
1. Glückwunsch! Der Bot funktioniert
2. Alle 8 Tests sollten PASS sein
3. Bereit für Raspberry Pi Installation
4. → Siehe RASPBERRY_PI_SETUP.md
```

### ✗ Fehler bei einem Test?
```
1. Notiere die Fehlermeldung
2. Schaue in Troubleshooting
3. Installiere fehlende Pakete
4. Versuche Test erneut
5. Falls immer noch Fehler → GitHub Issue
```

---

## 💡 Tipps für Tieferes Verständnis

### 1. Code während Test lesen
```
Öffne während Test diese Dateien parallel:
- src/trading_engine.py
- src/risk_manager.py
- src/backtest.py

Verstehe wie sie zusammenarbeiten
```

### 2. Demo-Code modifizieren
```python
# In demo_bot.py:
# Ändere Entry Price
entry = 200  # Statt 150

# Oder ändere Position Size
qty = 500    # Statt berechnet

# Oder ändere Stop Loss %
sl = rm.calculate_stop_loss(entry, 0.10)  # 10% statt 5%

# Dann erneut ausführen und Unterschied sehen!
```

### 3. Backtesting mit eigener Strategie
```python
# Erstelle eigenes Signal-System
# z.B. RSI-basiert, MACD, etc.
# Dann mit BacktestEngine testen
```

---

## 🔒 Wichtige Sicherheitshinweise

**Vor echter Verwendung:**

1. ⚠️ **Alles ist Paper Trading!**
   - Keine echten Trades
   - Kein Geld verwendet
   - Nur zum Lernen

2. ⚠️ **API Keys niemals hardcoden!**
   - Nutze Umgebungsvariablen
   - Oder .env Datei mit chmod 600
   - Nie in GitHub committen

3. ⚠️ **Erst 3 Monate Paper Trading!**
   - Dann Backtesting machen
   - Dann Micro Trading (50-100$)
   - Nur dann skalieren

---

## 📚 Dokumentation

| Datei | Für wen | Inhalt |
|-------|---------|--------|
| `LAPTOP_TESTING.md` | Dich jetzt | Detaillierte Test-Anleitung |
| `BOT_README.md` | Bot-Nutzer | Bot Features & Nutzung |
| `RASPBERRY_PI_SETUP.md` | Pi-User | Pi Installation |
| `.env` | Admin | Bot-Konfiguration |

---

## 🎮 Kommandos Quick-Reference

```bash
# Test Suite (alle Tests)
python test_bot_locally.py

# Interaktive Demo
python demo_bot.py

# Einzelne Demos
python demo_bot.py workflow    # Trading Workflow
python demo_bot.py backtest    # Backtesting
python demo_bot.py risk        # Risk Szenarien

# Mit Virtual Environment aktiviert
source trading_env/bin/activate  # macOS/Linux
trading_env\Scripts\activate     # Windows

# Deaktivieren
deactivate

# Requirements erneuern
pip install -r requirements.txt --force-reinstall

# Bot später starten (auf Laptop)
python pi_bot_main.py          # Nicht auf echtem Laptop!
```

---

## ✅ Checkliste vor Pi-Installation

- [ ] `python test_bot_locally.py` erfolgreich
- [ ] Alle 8 Tests: `PASS`
- [ ] `demo_bot.py` läuft ohne Fehler
- [ ] Backtesting-Ergebnisse verstanden
- [ ] Risk-Szenarien klar
- [ ] `.env` Datei konfiguriert
- [ ] Bereit für Raspberry Pi

---

## 🚀 Nächster Schritt

Wenn alle Tests erfolgreich:

1. Lese `BOT_README.md` für Bot-Features
2. Konfiguriere `.env` für deine Aktien
3. Folge `RASPBERRY_PI_SETUP.md` für Pi-Installation
4. Starte mit Paper Trading
5. Nach 3 Monaten: Optional echte Trades

---

**Viel Erfolg! 🎯**

Bei Fragen: Siehe Dokumentation oder GitHub Issues
