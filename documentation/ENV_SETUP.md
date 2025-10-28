# Environment Variables Setup (Sicherheit) 🔐

## Übersicht

Statt deine geheimen Schlüssel direkt im Code zu speichern, benutzen wir `.env` Dateien:

```
❌ NICHT SICHER:
config = {
    'api_key': 'pk_live_xxxxxxxxxxxxx',  # Exposed in Git!
}

✅ SICHER:
# In .env Datei
ALPACA_API_KEY=pk_live_xxxxxxxxxxxxx

# In Python Code
from src.env_loader import get
api_key = get('ALPACA_API_KEY')
```

---

## 1. Installation (einmalig)

### Schritt 1: python-dotenv installieren

```bash
pip install python-dotenv
```

Oder aktualisiere dein bestehendes Setup:

```bash
pip install -r requirements.txt --upgrade
```

### Schritt 2: .env Datei erstellen

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### Schritt 3: .env mit echten Werten ausfüllen

Öffne `.env` und ersetze alle `your_xxxxx_here` Werte mit echten Daten.

---

## 2. Environment Variables - Wo bekomme ich sie?

### 🚀 Alpaca API Keys

1. Besuche: **https://alpaca.markets**
2. Registriere dich oder melde dich an
3. Gehe zu: **Dashboard → API Keys**
4. Kopiere:
   - **API Key** → `ALPACA_API_KEY=`
   - **Secret Key** → `ALPACA_SECRET_KEY=`

```env
ALPACA_API_KEY=pk_live_xxxxxxxxxxxxx
ALPACA_SECRET_KEY=sk_live_xxxxxxxxxxxxx
```

**Tipp:** Nutze Paper Trading Account für Tests!

---

### 📧 Email Notifications (Gmail)

1. Besuche: **https://myaccount.google.com/apppasswords**
   - *(Du musst 2-Factor-Auth aktiviert haben)*
2. Wähle:
   - **Select app:** Mail
   - **Select device:** Windows Computer (oder dein Device)
3. **Generiere** - Google erstellt ein 16-stelliges Passwort
4. Kopiere das Passwort:

```env
EMAIL_ADDRESS=dein_email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

**WICHTIG:** Das ist KEIN dein normales Gmail-Passwort!

---

### 📱 Telegram Notifications

#### Schritt 1: Bot erstellen

1. Öffne Telegram
2. Suche nach: `@BotFather`
3. Schreib: `/newbot`
4. Folge den Anweisungen
5. `BotFather` gibt dir einen **Bot Token**

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

#### Schritt 2: Chat ID finden

1. Schreib eine Nachricht an deinen neuen Bot
2. Öffne den Link: 
   ```
   https://api.telegram.org/bot[TOKEN]/getUpdates
   ```
   *(Ersetze [TOKEN] mit deinem Bot Token)*
3. Suche nach `"chat"` - kopiere die `"id"` Nummer

```env
TELEGRAM_CHAT_ID=123456789
```

**Beispiel Response:**
```json
{
  "ok": true,
  "result": [
    {
      "message": {
        "chat": {
          "id": 123456789,  # ← Das ist deine Chat ID
          "first_name": "Max"
        }
      }
    }
  ]
}
```

---

## 3. .env Datei konfigurieren

### Vollständiges Beispiel

```env
# ============================================
# Alpaca API Credentials (ERFORDERLICH)
# ============================================
ALPACA_API_KEY=pk_live_xxxxxxxxxxxxx
ALPACA_SECRET_KEY=sk_live_xxxxxxxxxxxxx

# ============================================
# Email Notifications (Optional)
# ============================================
EMAIL_ADDRESS=dein_email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

# ============================================
# Telegram Notifications (Optional)
# ============================================
TELEGRAM_BOT_TOKEN=123:ABCde...
TELEGRAM_CHAT_ID=987654321

# ============================================
# Trading Config (Optional, default OK)
# ============================================
TRADING_SYMBOLS=AAPL,GOOGL,MSFT,AMZN
PAPER_TRADING=true
RISK_PER_TRADE=0.02

# ============================================
# System Config (Optional)
# ============================================
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 4. Im Python Code benutzen

### Methode 1: env_loader Modul (EMPFOHLEN)

```python
from src.env_loader import get, get_bool, get_int

# String Variable
api_key = get('ALPACA_API_KEY')

# Boolean Variable
paper_trading = get_bool('PAPER_TRADING', default=True)

# Integer Variable
max_positions = get_int('MAX_POSITIONS', default=5)

# Mit Fehlerprüfung
required_key = get('ALPACA_API_KEY', required=True)
# Wirft ValueError wenn nicht gesetzt!
```

### Methode 2: Direkt os.environ

```python
import os

# Hier werden .env Werte automatisch geladen (wenn dotenv installiert)
api_key = os.getenv('ALPACA_API_KEY')
```

---

## 5. Sicherheit - Best Practices

### ✅ DO's

```python
# ✓ Nutze env_loader für Laden
from src.env_loader import get
api_key = get('ALPACA_API_KEY')

# ✓ Nutze separate .env für Entwicklung & Produktion
# .env (Dein lokales Setup)
# .env.production (Pi Setup - unterschiedliche Keys!)

# ✓ .env in .gitignore (schon done!)
# .gitignore enthält: .env

# ✓ Nutze Umgebungsvariablen auf Production
# System → Umgebungsvariablen setzen
# export ALPACA_API_KEY="xxxxx"

# ✓ Begrenzte API Key Berechtigungen
# Alpaca: Nutze Paper Trading Account für Tests
# Gmail: Nutze App Password (nicht echtes Passwort)
```

### ❌ DON'Ts

```python
# ✗ NIEMALS Keys in Code hardcoden
api_key = "pk_live_xxxxxxxxxxxxx"

# ✗ NIEMALS Keys in Git committen
git add config.json  # Datei enthält Keys!

# ✗ NIEMALS Keys in Logs ausgeben
logger.info(f"Using key: {api_key}")

# ✗ NIEMALS .env.example mit echten Werten committen
# .env.example = Template nur
# .env = echte Werte (NICHT in Git!)
```

---

## 6. Fehlerbehandlung

### Fehler: ModuleNotFoundError: No module named 'dotenv'

```bash
pip install python-dotenv
```

### Fehler: Environment variable not found

```python
from src.env_loader import get

# Mit Default Value
api_key = get('ALPACA_API_KEY', default='pk_test_default')

# Mit Fehler wenn nicht gesetzt
api_key = get('ALPACA_API_KEY', required=True)
# → ValueError wenn nicht gesetzt
```

### Fehler: .env wird nicht geladen

```python
from src.env_loader import init_env

# Explizit laden mit Pfad
init_env('.env')  # Aktuelles Verzeichnis

# Oder mit vollständigem Pfad
init_env('/path/to/.env')
```

### Debug: Welche Werte sind gesetzt?

```python
import os
from pathlib import Path

# Print alle ENV Variablen (Vorsicht: Passwörter!)
for key, value in os.environ.items():
    if 'ALPACA' in key or 'TOKEN' in key:
        print(f"{key} = {value[:5]}...")  # Nur erste 5 Zeichen
```

---

## 7. Verschiedene Umgebungen

### Struktur für mehrere .env Dateien

```
project/
├── .env                 # Dein Entwicklungs-Setup (NICHT in Git)
├── .env.example         # Template für alle (IN Git)
├── .env.production      # (Optional) Pi Production Setup
└── .env.testing         # (Optional) Test Setup
```

### Setup für verschiedene Umgebungen

```bash
# Development (auf Laptop)
cp .env.example .env
# Fülle mit deine Test-Keys

# Testing
cp .env.example .env.testing
# Fülle mit Test-Daten

# Production (auf Pi)
cp .env.example .env.production
# Fülle mit echten Production-Keys
```

### Im Code auswählen

```python
import os
from src.env_loader import init_env

# Umgebung aus ENVIRONMENT Variable
env = os.getenv('ENVIRONMENT', 'development')

# Lade entsprechende .env
if env == 'production':
    init_env('.env.production')
elif env == 'testing':
    init_env('.env.testing')
else:
    init_env('.env')
```

---

## 8. Checkliste - Setup komplett?

- [ ] `python-dotenv` installiert (`pip install python-dotenv`)
- [ ] `.env` Datei erstellt (`cp .env.example .env`)
- [ ] `.env` mit Alpaca Keys gefüllt
- [ ] `.env` in `.gitignore` (schon erledigt)
- [ ] `env_loader.py` in `src/` existiert
- [ ] Test läuft: `python test_bot_locally.py`
- [ ] Keine Keys im Code hardcoded

---

## 9. Testen ob alles funktioniert

### Test 1: .env wird geladen

```bash
python -c "from src.env_loader import get; print('API Key:', get('ALPACA_API_KEY', 'NOT SET'))"
```

**Erwartet:** Dein echtes API Key (oder "NOT SET" wenn leer)

### Test 2: env_loader im Bot

```bash
python pi_bot_main.py --test
```

**Erwartet:** Bot startet ohne "KEY NOT FOUND" Fehler

### Test 3: In Python interaktiv

```python
from src.env_loader import get, get_bool

# Alle Variablen checken
print("API Key:", get('ALPACA_API_KEY', 'NOT SET')[:10] + "...")
print("Paper Trading:", get_bool('PAPER_TRADING'))
print("Email:", get('EMAIL_ADDRESS', 'NOT SET'))
print("Telegram:", get('TELEGRAM_BOT_TOKEN', 'NOT SET')[:10] + "...")
```

---

## 10. Auf Raspberry Pi nutzen

### Option A: .env Datei (wie auf Laptop)

```bash
# Pi Setup
scp .env pi@raspberry:/home/pi/BigDataProject/
cd /home/pi/BigDataProject
python pi_bot_main.py
```

### Option B: Umgebungsvariablen (besser für Production)

```bash
# Pi - Systemweit setzen
export ALPACA_API_KEY="pk_live_xxxxx"
export ALPACA_SECRET_KEY="sk_live_xxxxx"
# usw...

# Oder in Systemd Service (.env.service):
[Service]
Environment="ALPACA_API_KEY=pk_live_xxxxx"
Environment="ALPACA_SECRET_KEY=sk_live_xxxxx"
```

---

## 11. Häufige Fehler

| Fehler | Ursache | Lösung |
|--------|--------|--------|
| `ModuleNotFoundError: dotenv` | python-dotenv nicht installiert | `pip install python-dotenv` |
| `KeyError: 'ALPACA_API_KEY'` | Variable in .env nicht gesetzt | Prüfe .env Datei |
| `.env wird ignoriert` | DOTENV_AVAILABLE = False | Prüfe Python PATH |
| `ValueError: required variable not set` | required=True aber Variable leer | Fülle Wert in .env |
| Keys in Git uploaded | .env nicht in .gitignore | Manually remove from Git history |

---

## 12. Weitere Ressourcen

- **python-dotenv Docs:** https://python-dotenv.readthedocs.io/
- **Alpaca API:** https://alpaca.markets
- **Gmail App Passwords:** https://myaccount.google.com/apppasswords
- **Telegram Bot API:** https://core.telegram.org/bots/api

---

**Sicher? ✅ Dann kann's losgehen! 🚀**

Nächste Schritte:
1. `.env` Datei mit deinen Keys füllen
2. `python test_bot_locally.py` ausführen
3. Bot auf Raspberry Pi testen

