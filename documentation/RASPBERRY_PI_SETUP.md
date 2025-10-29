# Raspberry Pi Trading Bot - Setup Guide

## Systemanforderungen

### Hardware
- **Raspberry Pi 4** (empfohlen): 4GB RAM, beste Performance
- **Raspberry Pi 3B+**: 1GB RAM, funktioniert aber langsamer
- **Raspberry Pi Zero 2**: 512MB RAM, sehr begrenzt
- **SD-Karte**: Mindestens 32GB (Class 10)
- **Stromversorgung**: 5V/2.5A Netzteil

### Software
- **OS**: Raspberry Pi OS (Bullseye oder später)
- **Python**: 3.9 oder höher
- **Internet**: Stabiler Internetzugang (für API Zugriff)

---

## Schritt 1: Raspberry Pi OS Installation

```bash
# Auf einem anderen Computer:
# 1. Raspberry Pi Imager herunterladen: https://www.raspberrypi.com/software/
# 2. SD-Karte einlegen
# 3. Raspberry Pi OS (64-bit) wählen
# 4. Schreiben und fertig
```

---

## Schritt 2: Basis-Konfiguration auf dem Pi

```bash
# SSH aktivieren (falls noch nicht geschehen)
sudo raspi-config
# Interface Options → SSH → Ja

# System aktualisieren
sudo apt update
sudo apt upgrade -y

# Notwendige Pakete installieren
sudo apt install -y python3-pip python3-venv git
```

---

## Schritt 3: Trading Bot Herunterladen

```bash
# Home Verzeichnis
cd ~

# Repository klonen
git clone https://github.com/brittojo7n/BigDataProject-StockMarketTrendAnalysisAndPrediction.git
cd BigDataProject-StockMarketTrendAnalysisAndPrediction

# Oder manuell hochladen via SFTP/SCP
```

---

## Schritt 4: Python Umgebung Setup

```bash
# Virtuelle Umgebung erstellen
python3 -m venv trading_env

# Aktivieren
source trading_env/bin/activate

# Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

# Zusätzliche Trading-Pakete
pip install alpaca-trade-api schedule

# Optional: Für Telegram/Email
pip install python-telegram-bot

# Optional: Leichtgewichtige TensorFlow Version (für Pi Zero)
pip install tensorflow-lite
```

### Problem: TensorFlow zu groß für Raspberry Pi Zero?

```bash
# Alternative: TensorFlow Lite (600MB statt 2GB)
pip uninstall tensorflow
pip install tensorflow-lite

# Oder: Nur NumPy/Pandas für einfachere Strategien
pip install numpy pandas scikit-learn
```

---

## Schritt 5: Alpaca API Konfiguration

### Konto erstellen:
1. Gehe zu https://alpaca.markets
2. Registriere dich
3. Erstelle ein API Key/Secret Paar
4. Nutze zunächst **Paper Trading** (simuliert mit echten Daten)

### Umgebungsvariablen setzen:

```bash
# Datei erstellen/editieren
nano ~/.bashrc

# Am Ende hinzufügen:
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_SECRET_KEY="your_secret_key_here"
export TELEGRAM_BOT_TOKEN="your_bot_token_here"  # Optional
export TELEGRAM_CHAT_ID="your_chat_id_here"      # Optional

# Speichern: Ctrl+X, Y, Enter

# Laden
source ~/.bashrc

# Verifizieren
echo $ALPACA_API_KEY
```

### Sicherer: Datei-basiert

```bash
# Erstelle config/secrets.env
mkdir -p config
cat > config/secrets.env << EOF
ALPACA_API_KEY="your_key"
ALPACA_SECRET_KEY="your_secret"
TELEGRAM_BOT_TOKEN="optional"
TELEGRAM_CHAT_ID="optional"
EOF

# Nur für Dich lesbar
chmod 600 config/secrets.env

# In Bot laden:
set -a
source config/secrets.env
set +a
```

---

## Schritt 6: Bot Konfigurieren

```bash
# Umgebungsvariablen-Datei bearbeiten
nano .env

# Wichtige Einstellungen:
# - PAPER_TRADING=true (zuerst!)
# - TRADING_SYMBOLS=AAPL,MSFT,GOOGL (welche Aktien sollen gehandelt werden)
# - RISK_PER_TRADE=2 (wie viel pro Trade riskieren in %)
# - ANALYSIS_TIME="09:30" (wann sollen Analysen laufen)
# - LIGHTWEIGHT_MODE=true (für Pi Zero/3)
```

---

## Schritt 7: Erste Testläufe

```bash
# Umgebung aktivieren
source trading_env/bin/activate

# Bot im Test-Modus starten
python pi_bot_main.py

# Logs beobachten
tail -f trading_bot.log

# Mit Ctrl+C beenden
```

### Was sollte passieren:
1. Bot verbindet sich zu Alpaca
2. Lädt aktuelle Daten
3. Generiert Signale
4. (Mock)-Trades ausführen (Paper Trading)
5. Logs anzeigen

---

## Schritt 8: Als Systemdienst Einrichten (Optional)

```bash
# Systemd Service Datei erstellen
sudo nano /etc/systemd/system/trading-bot.service
```

Inhalt:
```ini
[Unit]
Description=Trading Bot for Raspberry Pi
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/BigDataProject-StockMarketTrendAnalysisAndPrediction
Environment="PATH=/home/pi/BigDataProject-StockMarketTrendAnalysisAndPrediction/trading_env/bin"
EnvironmentFile=/home/pi/config/secrets.env
ExecStart=/home/pi/BigDataProject-StockMarketTrendAnalysisAndPrediction/trading_env/bin/python pi_bot_main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Dann:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Aktivieren
sudo systemctl enable trading-bot

# Starten
sudo systemctl start trading-bot

# Status prüfen
sudo systemctl status trading-bot

# Logs anschauen
sudo journalctl -u trading-bot -f
```

---

## Schritt 9: Tägliche Logs Verwalten

```bash
# Logs-Ordner erstellen
mkdir -p logs

# Log-Rotation einrichten
sudo nano /etc/logrotate.d/trading-bot
```

Inhalt:
```
/home/pi/BigDataProject-StockMarketTrendAnalysisAndPrediction/logs/trading_bot.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## Schritt 10: Benachrichtigungen (Optional)

### Telegram Bot erstellen:

```bash
# 1. BotFather Telegram Bot öffnen: @BotFather
# 2. /newbot eingeben
# 3. Namen für Bot eingeben
# 4. Token kopieren

# 2. Chat ID finden:
# - Telegram App öffnen
# - Mit Deinem Bot chatten (/start)
# - https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates aufrufen
# - Chat ID finden

# 3. In Konfiguration setzen:
export TELEGRAM_BOT_TOKEN="123456789:ABCdefgh..."
export TELEGRAM_CHAT_ID="123456789"
```

### Gmail Benachrichtigungen:

```bash
# 1. 2-Faktor-Authentifizierung aktivieren
# 2. App-Passwort generieren: https://myaccount.google.com/apppasswords
# 3. In .env:

EMAIL_ENABLED=true
EMAIL_RECIPIENT=dein_email@gmail.com
EMAIL_PASSWORD=dein_app_passwort
```

---

## Schritt 11: Backtesting vor echten Trades

```bash
# Backtest-Script ausführen
python -c "
from src.backtest import BacktestEngine
from src.data_fetching import get_closing_prices

# Daten laden
prices = get_closing_prices(['AAPL'])

# Einfaches Backtest
engine = BacktestEngine()
# ... mehr Code
"
```

---

## Problembehebung

### Problem: "Import tensorflow failed"
```bash
# Nur auf Pi Zero/3 nötig
pip install tensorflow-lite
# Oder Strategie ohne LSTM verwenden
```

### Problem: "Bot verbindet sich nicht zu Alpaca"
```bash
# API Keys prüfen
echo $ALPACA_API_KEY

# Internetzugang testen
ping 8.8.8.8

# Alpaca Status: https://status.alpaca.markets
```

### Problem: "Bot verbraucht zu viel RAM"
```bash
# In .env:
LIGHTWEIGHT_MODE=true
CPU_ONLY=true

# Modell-Einstellungen in .env reduzieren:
LSTM_UNITS=10  # Statt 25
LSTM_EPOCHS=1  # Statt 5
```

### Problem: "Performance zu langsam"
```bash
# 1. Weniger Symbole in .env (TRADING_SYMBOLS)
# 2. Längere Check-Intervalle
# 3. CPU Clock erhöhen (vorsicht: Wärme)
sudo nano /boot/config.txt
# Hinzufügen: arm_freq=1800  # für Pi 4
```

---

## Monitoring & Wartung

### Regelmäßige Checks

```bash
# Disk-Speicher prüfen
df -h

# RAM-Nutzung prüfen
free -h

# Temperatur prüfen
vcgencmd measure_temp

# Bot-Prozess prüfen
ps aux | grep python
```

### Backup erstellen

```bash
# Trades und Logs sichern
tar -czf ~/bot_backup_$(date +%Y%m%d).tar.gz \
  ~/BigDataProject-StockMarketTrendAnalysisAndPrediction/data \
  ~/BigDataProject-StockMarketTrendAnalysisAndPrediction/logs
```

### Updates installieren

```bash
cd ~/BigDataProject-StockMarketTrendAnalysisAndPrediction
git pull origin main
source trading_env/bin/activate
pip install --upgrade -r requirements.txt
```

---

## Sicherheit

⚠️ **WICHTIG: Paper Trading zuerst!**

1. Starte mit **Paper Trading** (simulated)
2. Laufe mindestens **3 Monate** im Test
3. Überprüfe Logs täglich
4. Teste mit **kleinen Beträgen** ($50-200)
5. Aktiviere **Stop Losses**
6. Setze **Max Daily Loss** Limit

### API Key Sicherheit

```bash
# NIEMALS hardcoden!
# ✓ Umgebungsvariablen verwenden
# ✓ .env Datei mit chmod 600
# ✗ Nicht in GitHub committen

# .gitignore:
echo "config/secrets.env" >> .gitignore
echo "*.log" >> .gitignore
echo "data/" >> .gitignore
```

---

## Nächste Schritte

1. **Backtest**: Strategie testen
2. **Paper Trading**: 3+ Monate mit echten Daten (aber kein Geld)
3. **Micro Trading**: $50-100 auf echtem Konto
4. **Scale Up**: Nur wenn konsistent profitabel
5. **Monitoring**: Täglich Logs überprüfen

---

## Support & Ressourcen

- Alpaca API Docs: https://alpaca.markets/docs/
- Raspberry Pi Docs: https://www.raspberrypi.com/documentation/
- Bot Logs: `cat trading_bot.log`
- Community: GitHub Issues

---

**Erstellt**: 2025-10-28  
**Version**: 1.0  
**Status**: Produktionsreife
