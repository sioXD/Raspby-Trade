# Trading Bot auf Laptop testen

## 🚀 Schnellstart

### Option 1: Automatisierte Test-Suite (Empfohlen)

```bash
# Alle Tests ausführen
python test_bot_locally.py
```

Das Script testet automatisch:
- ✅ Data Fetching (Yahoo Finance)
- ✅ Stock Analysis
- ✅ Correlations
- ✅ Risk Management
- ✅ Trading Engine
- ✅ Notifications
- ✅ Backtesting
- ✅ Monte Carlo

**Ergebnis:** Detaillierter Report mit Pass/Fail für jeden Test

---

### Option 2: Interaktive Demo

```bash
# Mit interaktivem Menü
python demo_bot.py

# Oder direkt eine Demo:
python demo_bot.py workflow    # Trading Workflow
python demo_bot.py backtest    # Backtesting
python demo_bot.py risk        # Risk Szenarien
```

---

## 📋 Was wird getestet?

### Test 1: DATA FETCHING
```
✓ Lädt aktuelle Daten von Yahoo Finance
✓ Prüft auf Fehler bei Datenbeschaffung
✓ Zeigt Datenpunkte und Shape
```

### Test 2: STOCK ANALYSIS
```
✓ Berechnet Moving Averages (10, 20, 50 Tage)
✓ Berechnet tägliche Returns
✓ Zeigt Statistiken
```

### Test 3: CORRELATION ANALYSIS
```
✓ Analysiert Korrelationen zwischen Aktien
✓ Erstellt Korrelationsmatrix
✓ Zeigt Abhängigkeiten
```

### Test 4: RISK MANAGEMENT
```
✓ Berechnet Position Size basierend auf Risiko
✓ Kalkuliert Stop Loss & Take Profit
✓ Validiert Trades
✓ Verwaltet offene Positionen
```

### Test 5: TRADING ENGINE
```
✓ Initialisiert in Mock-Mode
✓ Führt simulierte Orders aus (BUY/SELL)
✓ Führt Order-Log
✓ Keine echten Trades!
```

### Test 6: NOTIFIER
```
✓ Prüft Notification System
✓ Email & Telegram konfigurierbar
✓ Keine echten Benachrichtigungen gesendet
```

### Test 7: BACKTESTING
```
✓ Teste Strategie auf historischen Daten
✓ Berechne Win Rate, Sharpe Ratio, Drawdown
✓ Zeige beste/schlechteste Trades
✓ KEIN echtes Geld verwendet!
```

### Test 8: MONTE CARLO SIMULATION
```
✓ Simuliert zukünftige Kursverläufe
✓ Berechnet Value at Risk
✓ Zeigt mögliche Szenarien
```

---

## 💻 System-Anforderungen

```
Mindestens:
- Windows/Mac/Linux
- Python 3.8+
- 2GB RAM
- Internetzugang (für Yahoo Finance API)

Installation:
```bash
python -m pip install -r requirements.txt
```
```

---

## 📊 Demo Beschreibungen

### DEMO 1: Trading Workflow

Simuliert einen kompletten Handelstag:

```
[SCHRITT 1] Lade Aktiendaten
  → Lädt AAPL, GOOGL, MSFT

[SCHRITT 2] Zeige aktuelle Preise
  → AAPL: $195.50 (+2.15%)
  → GOOGL: $140.25 (-0.75%)
  → MSFT: $380.00 (+1.50%)

[SCHRITT 3] Starte Trading Engine
  → Account Balance: $100,000
  → Risk per Trade: 2% ($2,000)

[SCHRITT 4] Simuliere Trading-Szenario
  → AAPL: BULLISH Signal (85% Confidence)
    Entry: $195.50, SL: $185.73, TP: $214.95
    Position: 52 shares
    ✓ Order gefüllt

  → GOOGL: BULLISH Signal (72% Confidence)
    Entry: $140.25, SL: $133.24, TP: $154.28
    Position: 71 shares
    ✓ Order gefüllt

[SCHRITT 5] Risiko-Übersicht
  → Open Positions: 2
    AAPL: 52 shares @ $195.50
    GOOGL: 71 shares @ $140.25
  → Total Risk: $2,071.20 (2.07%)
  → Status: OK

[SCHRITT 6] Trade Log
  → 1. BUY AAPL - 52 shares
  → 2. BUY GOOGL - 71 shares
```

### DEMO 2: Backtesting

Teste Strategie auf echten historischen Daten:

```
[SCHRITT 1] Lade historische Daten (AAPL)
  → 252 Datenpunkte (letzte 1 Jahr)

[SCHRITT 2] Generiere Signale (Simple MA Strategie)
  → 10-Tage MA vs 50-Tage MA
  → 126 BUY Signale
  → 126 SELL Signale

[SCHRITT 3] Starte Backtest
  → Initial Balance: $100,000

[SCHRITT 4] Ergebnisse:
  Final Balance:       $108,450
  Total Profit:        $8,450
  Total Return:        8.45%
  
  Total Trades:        42
  Winning Trades:      28 (66.67%)
  Losing Trades:       14 (33.33%)
  Win Rate:            66.67%
  
  Sharpe Ratio:        1.24
  Max Drawdown:        -8.50%

[SCHRITT 5] Top Gewinntrades:
  1. 2024-06-15: +$1,250.50 (+3.45%)
  2. 2024-07-22: +$890.75 (+2.10%)
  3. 2024-08-10: +$765.25 (+1.95%)
```

### DEMO 3: Risk Szenarien

Teste verschiedene Risiko-Situationen:

```
[SZENARIO 1] Normaler Trade
  Entry: $150, SL: $142.50, TP: $165
  Position: 267 shares
  Valid: True ✓

[SZENARIO 2] Zu großer Trade
  Position: 10,000 shares
  Valid: False ✗
  Reason: Risk ($50,000) exceeds max ($2,000)

[SZENARIO 3] Max Positionen erreicht
  Max: 2, Current: 2
  Valid: False ✗
  Reason: Cannot open position in MSFT

[SZENARIO 4] Stop Loss wird ausgelöst
  Position: 100 shares @ $100
  Stop Loss: $95
  
  Preis $105: ✓ OK
  Preis $99:  ✓ OK
  Preis $95:  🔴 HIT!
  Preis $90:  🔴 HIT!
```

---

## 🔍 Detaillierte Testschritte

### 1. Alles testen

```bash
python test_bot_locally.py
```

**Output Beispiel:**
```
======================================================================
 TRADING BOT - LAPTOP TEST SUITE
======================================================================

============================================================
TEST 1: DATA FETCHING
============================================================
Lade Daten für AAPL, GOOGL, MSFT...
✓ Erfolgreich! 1260 Datenpunkte geladen
Shape: (1260, 3)

Letzte 5 Tage:
            AAPL    GOOGL     MSFT
2024-10-24 195.50  140.25  380.00
2024-10-25 197.30  141.50  381.75
...
```

### 2. Einzelne Tests

```bash
# Nur Backtesting
python -c "from test_bot_locally import test_backtest; test_backtest()"

# Nur Risk Management
python -c "from test_bot_locally import test_risk_management; test_risk_management()"
```

### 3. Debugging aktivieren

```bash
# Mit ausführlichem Logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from test_bot_locally import run_all_tests
run_all_tests()
"
```

---

## 🐛 Häufige Fehler & Lösungen

### Error: "Import yfinance failed"
```bash
pip install yfinance
```

### Error: "API rate limit exceeded"
```
Yahoo Finance hat ein Rate Limit. Warte 1 Minute und versuche erneut.
```

### Error: "No data returned for AAPL"
```
- Internetverbindung prüfen
- Yahoo Finance Status: finance.yahoo.com
- Später nochmal versuchen
```

### Error: "TensorFlow not found"
```bash
pip install tensorflow
# Oder für Pi Zero:
pip install tensorflow-lite
```

---

## 📈 Nächste Schritte nach dem Test

1. **✓ Tests erfolgreich?**
   ```
   → Gut! Der Bot funktioniert auf deinem Laptop
   → Bereit für Raspberry Pi Installation
   ```

2. **✗ Fehler bei Tests?**
   ```
   → Schau in Fehlermeldungen
   → Installiere fehlende Pakete
   → Versuche erneut
   ```

3. **Konfiguration überprüfen**
   ```bash
   nano config.yaml
   # Stelle sicher:
   # - use_paper_trading: true
   # - symbols: gewünschte Aktien
   # - risk_per_trade: 0.02 (2%)
   ```

4. **Backtesting durchführen**
   ```bash
   python -c "from demo_bot import demo_backtesting; demo_backtesting()"
   ```

5. **Auf Raspberry Pi deployen**
   ```
   Wenn alles funktioniert:
   → Siehe RASPBERRY_PI_SETUP.md
   ```

---

## 📝 Test-Checkliste

- [ ] `test_bot_locally.py` erfolgreich ausgeführt
- [ ] Alle 8 Tests bestanden
- [ ] `demo_bot.py` läuft ohne Fehler
- [ ] Backtesting-Demo sieht sinnvoll aus
- [ ] Risk-Szenarien verstanden
- [ ] config.yaml konfiguriert
- [ ] API Keys gesetzt (für echten Bot)
- [ ] Bereit für Raspberry Pi Installation

---

## 🎓 Was du gelernt hast

Nach diesen Tests verstehst du:

- ✅ Wie der Bot Daten lädt
- ✅ Wie Signale generiert werden
- ✅ Wie Risk Management funktioniert
- ✅ Wie Orders ausgeführt werden (mock)
- ✅ Wie Benachrichtigungen funktionieren
- ✅ Wie Backtesting hilft Strategien zu testen
- ✅ Wie Risk Szenarien gehandhabt werden

---

## 💡 Tipps

**Für besseres Verständnis:**
1. Lese die Docstrings in den Source Files
2. Füge Breakpoints ein und debugge
3. Modifiziere die Demo-Skripte
4. Teste mit verschiedenen Symbolen

**Performance:**
- Erste Test-Suite dauert ~3-5 Minuten
- Backtesting dauert ~2-3 Minuten
- Risk-Szenarien dauert <1 Minute

---

## 📞 Support

Falls Fehler auftreten:
1. Lese die Fehlermeldung sorgfältig
2. Prüfe `test_bot_locally.py` Ausgabe
3. Überprüfe Python-Version (`python --version`)
4. Überprüfe Abhängigkeiten (`pip list`)
5. Versuche Neuinstallation: `pip install -r requirements.txt --force-reinstall`

---

**Viel Erfolg beim Testen! 🚀**

Wenn alles funktioniert: → Zum Raspberry Pi Setup gehen
