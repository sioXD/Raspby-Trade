#!/usr/bin/env python3
"""
Setup Helper - Erstellt .env Datei interaktiv
Fragt nach Keys und speichert sie sicher
"""

import os
import sys
from pathlib import Path


def print_header():
    print("\n" + "=" * 60)
    print("🔐 Trading Bot - Environment Variables Setup")
    print("=" * 60)


def print_section(title):
    print(f"\n\n{'─' * 60}")
    print(f"📋 {title}")
    print('─' * 60)


def get_input(prompt, secret=False, required=False):
    """Hole Input vom User"""
    while True:
        try:
            if secret:
                import getpass
                value = getpass.getpass(prompt)
            else:
                value = input(prompt)
            
            if required and not value.strip():
                print("⚠ Diese Variable ist erforderlich!")
                continue
            
            return value.strip()
        except KeyboardInterrupt:
            print("\n\n⏹ Setup abgebrochen")
            sys.exit(0)


def setup_env():
    """Interaktives Setup"""
    print_header()
    
    env_file = Path(".env")
    
    # Warnung wenn .env existiert
    if env_file.exists():
        print(f"\n⚠ .env Datei existiert bereits!")
        response = input("Möchtest du sie überschreiben? (y/N): ").lower()
        if response != 'y':
            print("Abgebrochen")
            return
    
    # Sammle Variablen
    config = {}
    
    # ==========================================
    # Alpaca API
    # ==========================================
    print_section("1️⃣ ALPACA API KEYS")
    print("Hol dir deine Keys von: https://alpaca.markets")
    print("1. Dashboard → API Keys")
    print("2. Kopiere API Key und Secret Key")
    
    config['ALPACA_API_KEY'] = get_input(
        "\n🔑 ALPACA_API_KEY (Paper Trading Key): ",
        required=True
    )
    config['ALPACA_SECRET_KEY'] = get_input(
        "🔑 ALPACA_SECRET_KEY: ",
        secret=True,
        required=True
    )
    
    # ==========================================
    # Email Notifications
    # ==========================================
    print_section("2️⃣ EMAIL NOTIFICATIONS (Optional)")
    enable_email = input("Möchtest du Email Benachrichtigungen? (y/N): ").lower() == 'y'
    
    if enable_email:
        print("\nHinweis: Nutze Gmail mit App Password!")
        print("Siehe: https://myaccount.google.com/apppasswords")
        
        config['EMAIL_ADDRESS'] = get_input(
            "\n📧 Gmail Adresse: ",
            required=True
        )
        config['EMAIL_PASSWORD'] = get_input(
            "📧 16-stelliges App Password: ",
            secret=True,
            required=True
        )
    else:
        config['EMAIL_ADDRESS'] = ""
        config['EMAIL_PASSWORD'] = ""
    
    # ==========================================
    # Telegram
    # ==========================================
    print_section("3️⃣ TELEGRAM NOTIFICATIONS (Optional)")
    enable_telegram = input("Möchtest du Telegram Benachrichtigungen? (y/N): ").lower() == 'y'
    
    if enable_telegram:
        print("\nHinweis: Erstelle einen Bot bei @BotFather")
        print("Siehe ENV_SETUP.md für detaillierte Anleitung")
        
        config['TELEGRAM_BOT_TOKEN'] = get_input(
            "\n🤖 Telegram Bot Token: ",
            required=True
        )
        config['TELEGRAM_CHAT_ID'] = get_input(
            "💬 Telegram Chat ID: ",
            required=True
        )
    else:
        config['TELEGRAM_BOT_TOKEN'] = ""
        config['TELEGRAM_CHAT_ID'] = ""
    
    # ==========================================
    # Trading Config
    # ==========================================
    print_section("4️⃣ TRADING CONFIGURATION (Optional)")
    
    symbols = input("\n📈 Trading Symbole (AAPL,GOOGL,MSFT,AMZN): ").strip()
    config['TRADING_SYMBOLS'] = symbols if symbols else "AAPL,GOOGL,MSFT,AMZN"
    
    paper_trading = input("Paper Trading nutzen? (Y/n): ").lower() != 'n'
    config['PAPER_TRADING'] = "true" if paper_trading else "false"
    
    risk = input("Risk per Trade (0.02): ").strip()
    config['RISK_PER_TRADE'] = risk if risk else "0.02"
    
    # ==========================================
    # System Config
    # ==========================================
    print_section("5️⃣ SYSTEM CONFIGURATION (Optional)")
    
    log_level = input("\nLog Level (INFO/DEBUG/WARNING): ").strip()
    config['LOG_LEVEL'] = log_level if log_level else "INFO"
    
    env_type = input("Environment (development/production): ").strip()
    config['ENVIRONMENT'] = env_type if env_type else "development"
    
    # ==========================================
    # Speichern
    # ==========================================
    print_section("💾 SPEICHERN")
    
    # Generiere .env Content
    env_content = "# Trading Bot Environment Variables\n"
    env_content += "# Erstellt von setup_env.py\n"
    env_content += "# WICHTIG: Nie in Git committen!\n\n"
    
    env_content += "# ============================================\n"
    env_content += "# Alpaca API Credentials (ERFORDERLICH)\n"
    env_content += "# ============================================\n"
    env_content += f"ALPACA_API_KEY={config['ALPACA_API_KEY']}\n"
    env_content += f"ALPACA_SECRET_KEY={config['ALPACA_SECRET_KEY']}\n"
    
    env_content += "\n# ============================================\n"
    env_content += "# Email Notifications\n"
    env_content += "# ============================================\n"
    env_content += f"EMAIL_ADDRESS={config['EMAIL_ADDRESS']}\n"
    env_content += f"EMAIL_PASSWORD={config['EMAIL_PASSWORD']}\n"
    
    env_content += "\n# ============================================\n"
    env_content += "# Telegram Notifications\n"
    env_content += "# ============================================\n"
    env_content += f"TELEGRAM_BOT_TOKEN={config['TELEGRAM_BOT_TOKEN']}\n"
    env_content += f"TELEGRAM_CHAT_ID={config['TELEGRAM_CHAT_ID']}\n"
    
    env_content += "\n# ============================================\n"
    env_content += "# Trading Configuration\n"
    env_content += "# ============================================\n"
    env_content += f"TRADING_SYMBOLS={config['TRADING_SYMBOLS']}\n"
    env_content += f"PAPER_TRADING={config['PAPER_TRADING']}\n"
    env_content += f"RISK_PER_TRADE={config['RISK_PER_TRADE']}\n"
    
    env_content += "\n# ============================================\n"
    env_content += "# System Configuration\n"
    env_content += "# ============================================\n"
    env_content += f"LOG_LEVEL={config['LOG_LEVEL']}\n"
    env_content += f"ENVIRONMENT={config['ENVIRONMENT']}\n"
    
    # Speichern
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        # Permissions setzen (nur Besitzer kann lesen)
        os.chmod(env_file, 0o600)
        
        print(f"\n✅ .env Datei erstellt: {env_file.absolute()}")
        print(f"🔒 Permissions: 600 (nur du kannst lesen)")
        
        # Verifizierung
        print("\n" + "=" * 60)
        print("📋 Gespeicherte Konfiguration:")
        print("=" * 60)
        
        for key, value in config.items():
            if value and 'SECRET' in key.upper() or 'PASSWORD' in key.upper():
                display = value[:5] + "***" if len(value) > 5 else "***"
            else:
                display = value if value else "(nicht gesetzt)"
            print(f"{key}: {display}")
        
        print("\n✅ Setup komplett!")
        print("\nNächste Schritte:")
        print("1. pip install -r requirements.txt")
        print("2. python test_bot_locally.py")
        print("3. python demo_bot.py")
        
    except Exception as e:
        print(f"\n❌ Fehler beim Speichern: {e}")
        sys.exit(1)


def main():
    """Main Entry Point"""
    try:
        setup_env()
    except KeyboardInterrupt:
        print("\n\n⏹ Setup abgebrochen")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
