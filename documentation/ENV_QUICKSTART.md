# 🔐 Environment Variables - Quick Start

Deine Keys sind jetzt **sicher** in einer `.env` Datei!

## ⚡ 2-Minuten Setup

### Schritt 1: python-dotenv installieren

```bash
pip install python-dotenv
```

Oder:
```bash
pip install -r requirements.txt
```

### Schritt 2: .env Datei erstellen

**Option A: Automatisch (EMPFOHLEN)**

```bash
python setup_env.py
```

Der Script fragt dich interaktiv nach:
- ✅ Alpaca API Keys
- ✅ Email Credentials (optional)
- ✅ Telegram Token (optional)
- ✅ Trading Settings

Speichert alles sicher in `.env`

---

**Option B: Manuell**

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Dann öffne `.env` und ersetze alle `your_xxxxx_here` mit echten Werten.

---

## 📝 Was wird benötigt?

### Erforderlich ✅

| Variable | Quelle | Länge |
|----------|--------|-------|
| `ALPACA_API_KEY` | https://alpaca.markets | ~20 Zeichen |
| `ALPACA_SECRET_KEY` | https://alpaca.markets | ~40 Zeichen |

### Optional 🟡

| Variable | Quelle |
|----------|--------|
| `EMAIL_ADDRESS` | Deine Gmail Adresse |
| `EMAIL_PASSWORD` | 16-stelliges App Password |
| `TELEGRAM_BOT_TOKEN` | @BotFather auf Telegram |
| `TELEGRAM_CHAT_ID` | Deine Telegram Chat ID |

---

## 🧪 Teste ob alles funktioniert

```bash
# Test 1: Lade .env
python -c "from src.env_loader import get; print('API Key:', get('ALPACA_API_KEY', 'NOT SET'))"

# Test 2: Bot startet mit .env
python pi_bot_main.py

# Test 3: Test Suite läuft
python test_bot_locally.py
```

---

## 🔒 Sicherheit

✅ **Was wurde gemacht:**
- `.env` in `.gitignore` → Nicht in Git
- `env_loader.py` maskiert Passwörter in Logs
- `setup_env.py` setzt Datei-Permissions auf 600
- API Keys werden NIE gelogged

❌ **Was NIE tun:**
- Keys in Code hardcoden
- Keys in `.env.example` speichern
- `.env` in Git committen
- Keys in Logs anzeigen

---

## 📚 Weitere Dokumentation

Detaillierte Anleitung: **ENV_SETUP.md**
- Schritt-für-Schritt Keys besorgen
- Fehlerbehandlung
- Multiple .env Dateien
- Production Setup

---

## 🚀 Nächste Schritte

```bash
# 1. python-dotenv installieren
pip install python-dotenv

# 2. .env erstellen
python setup_env.py

# 3. Teste Bot
python test_bot_locally.py

# 4. Interaktive Demos
python demo_bot.py
```

---

**Fertig? Dann kann's losgehen! 🎯**
