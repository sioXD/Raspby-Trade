#!/bin/bash
# Quick Start Script for Laptop Testing
# Führe aus: bash run_tests.sh (auf macOS/Linux)

echo "======================================================================"
echo " TRADING BOT - LAPTOP TEST SUITE SETUP"
echo "======================================================================"
echo ""

# Check Python
echo "[1/5] Prüfe Python Installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python gefunden: $PYTHON_VERSION"
else
    echo "✗ Python nicht gefunden!"
    echo "  Bitte installiere Python 3.8+ von python.org"
    exit 1
fi

# Create Virtual Environment
echo ""
echo "[2/5] Erstelle Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual Environment erstellt"
else
    echo "✓ Virtual Environment bereits vorhanden"
fi

# Activate Virtual Environment
echo ""
echo "[3/5] Aktiviere Virtual Environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo "✓ Virtual Environment aktiviert"
else
    echo "✗ Fehler beim Aktivieren des Virtual Environment"
    exit 1
fi

# Install Dependencies
echo ""
echo "[4/5] Installiere Dependencies aus requirements.txt..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "✗ Fehler beim pip upgrade"
    exit 1
fi
python3 -m pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installiert"
else
    echo "✗ Fehler bei Dependencies"
    exit 1
fi

# Run Tests
echo ""
echo "[5/5] Führe Test Suite aus..."
echo ""
python3 test_bot_locally.py

# Show Menu
echo ""
echo "✓ Test Suite abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "  1. Interaktive Demo:     python3 demo_bot.py"
echo "  2. Workflow Demo:        python3 demo_bot.py workflow"
echo "  3. Backtesting Demo:     python3 demo_bot.py backtest"
echo "  4. Risk Demo:            python3 demo_bot.py risk"
echo ""
echo "Dokumentation:"
echo "  - LAPTOP_TESTING.md      (Detaillierte Anleitung)"
echo "  - BOT_README.md          (Bot Features)"
echo "  - RASPBERRY_PI_SETUP.md  (Für Raspberry Pi)"
echo ""
