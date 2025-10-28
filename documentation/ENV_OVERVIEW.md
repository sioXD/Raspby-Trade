# 🔐 Environment Variables System - Übersicht

## Was wurde erstellt?

### 📁 Neue Dateien

```
✅ .env.example          Template mit allen Variablen (NO SECRETS!)
✅ setup_env.py          Interaktiver Setup-Script
✅ src/env_loader.py     Python Module zum Laden von .env
✅ ENV_SETUP.md          Detaillierte Dokumentation (Deutsch)
✅ ENV_QUICKSTART.md     Schnell-Anleitung
```

### ✏️ Aktualisierte Dateien

```
✅ requirements.txt      + python-dotenv hinzugefügt
✅ pi_bot_main.py        Nutzt jetzt env_loader statt os.getenv
✅ .gitignore            .env hinzugefügt (sicher!)
```

---

## 🚀 Wie benutzen?

### Variante A: Automatisch Setup (EMPFOHLEN)

```bash
# 1. Installiere Dependency
pip install python-dotenv

# 2. Starte interaktiven Setup
python setup_env.py

# Der Script fragt:
# → Alpaca API Key?
# → Alpaca Secret Key?
# → Email aktivieren? → Email & Password
# → Telegram? → Bot Token & Chat ID
# → Trading Symbole?
# → Paper Trading?
# → etc.

# Speichert alles in .env mit Permissions 600
```

### Variante B: Manuell (wenn du .env format kennst)

```bash
# 1. Kopiere Template
cp .env.example .env

# 2. Öffne und bearbeite
notepad .env

# 3. Ersetze alle your_xxxxx_here mit echten Werten
```

---

## 📖 Im Python Code nutzen

### Neue Methode (EMPFOHLEN)

```python
from src.env_loader import get, get_bool, get_int

# String
api_key = get('ALPACA_API_KEY')

# Boolean
use_paper = get_bool('PAPER_TRADING', default=True)

# Integer
max_pos = get_int('MAX_POSITIONS', default=5)

# Mit Fehler wenn nicht gesetzt
required_key = get('ALPACA_API_KEY', required=True)
```

### Alte Methode (funktioniert auch noch)

```python
import os

api_key = os.getenv('ALPACA_API_KEY')
```

---

## 🔒 Sicherheit

| Aspekt | Status | Details |
|--------|--------|---------|
| `.env` in Git | ✅ Sicher | In `.gitignore` |
| `.env.example` sauber | ✅ OK | Keine Secrets |
| Passwörter gemaskt | ✅ Ja | In Logs versteckt |
| File Permissions | ✅ 600 | Nur du kannst lesen |
| Keys hardcoded | ✅ Nein | Alle aus .env |

---

## 📋 Umgebungsvariablen

### Alpaca Trading (ERFORDERLICH)

```
ALPACA_API_KEY=pk_live_xxxxxxxxxxxxx
ALPACA_SECRET_KEY=sk_live_xxxxxxxxxxxxx
```

### Email Notifications (Optional)

```
EMAIL_ADDRESS=dein@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

### Telegram (Optional)

```
TELEGRAM_BOT_TOKEN=123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef
TELEGRAM_CHAT_ID=987654321
```

### Trading Config (Optional)

```
TRADING_SYMBOLS=AAPL,GOOGL,MSFT,AMZN
PAPER_TRADING=true
RISK_PER_TRADE=0.02
```

### System (Optional)

```
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 🧪 Teste ob Setup funktioniert

```bash
# Test 1: Module wird geladen
python -c "from src.env_loader import get; print('OK')"

# Test 2: Bot startet
python pi_bot_main.py

# Test 3: Test Suite
python test_bot_locally.py

# Test 4: Interaktive Demo
python demo_bot.py
```

---

## ❓ Häufige Fragen

### F: Wo speichere ich .env?

A: Im Root-Verzeichnis des Projekts (neben `pi_bot_main.py`)

### F: Was wenn ich .env vergesse?

A: Script warnt dich mit "⚠ .env Datei nicht gefunden"
Aber Bot funktioniert noch im Demo/Test Mode

### F: Kann ich .env auf Raspberry Pi nutzen?

A: Ja! `scp .env pi@raspberry:/home/pi/project/`

### F: Wie viele .env Dateien kann ich haben?

A: So viele wie du brauchst:
- `.env` (Development)
- `.env.production` (Pi Real Trading)
- `.env.testing` (Tests)

### F: Was wenn ich mein API Key vergesse?

A: Hole neuen Key von Alpaca: https://alpaca.markets

---

## 📚 Weitere Docs

- **ENV_SETUP.md** - Detaillierte Setup-Anleitung (Deutsch)
- **ENV_QUICKSTART.md** - 2-Minuten Quick-Start
- **.env.example** - Template mit allen Variablen
- **src/env_loader.py** - Python Module (mit Docstrings)

---

## 🎯 Workflow

```
1. pip install python-dotenv           ← Installiere Dependency
2. python setup_env.py                 ← Interaktiver Setup
3. python test_bot_locally.py          ← Teste Bot
4. python demo_bot.py                  ← Sehe Demos
5. python pi_bot_main.py               ← Starte Bot
```

---

**Fragen? Siehe ENV_SETUP.md für detaillierte Anleitung! 📖**
