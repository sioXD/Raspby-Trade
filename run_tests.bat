@echo off
REM Quick Start Script for Laptop Testing (Windows)
REM Führe aus: run_tests.bat

echo ======================================================================
echo  TRADING BOT - LAPTOP TEST SUITE SETUP
echo ======================================================================
echo.

REM Check Python
echo [1/5] Prüfe Python Installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✓ Python gefunden
) else (
    echo ✗ Python nicht gefunden!
    echo   Bitte installiere Python 3.8+ von python.org
    pause
    exit /b 1
)

REM Create Virtual Environment
echo.
echo [2/5] Erstelle Virtual Environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual Environment erstellt
) else (
    echo ✓ Virtual Environment bereits vorhanden
)

REM Activate Virtual Environment
echo.
echo [3/5] Aktiviere Virtual Environment...
call venv\Scripts\activate.bat
if %errorlevel% equ 0 (
    echo ✓ Virtual Environment aktiviert
) else (
    echo ✗ Fehler beim Aktivieren des Virtual Environment
    pause
    exit /b 1
)

REM Install Dependencies
echo.
echo [4/5] Installiere Dependencies aus requirements.txt...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ✗ Fehler beim pip upgrade
    pause
    exit /b 1
)
python -m pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo ✓ Dependencies installiert
) else (
    echo ✗ Fehler bei Dependencies
    pause
    exit /b 1
)

REM Run Tests
echo.
echo [5/5] Führe Test Suite aus...
echo.
python test_bot_locally.py

REM Show Menu
echo.
echo ✓ Test Suite abgeschlossen!
echo.
echo Nächste Schritte:
echo   1. Interaktive Demo:     python demo_bot.py
echo   2. Workflow Demo:        python demo_bot.py workflow
echo   3. Backtesting Demo:     python demo_bot.py backtest
echo   4. Risk Demo:            python demo_bot.py risk
echo.
echo Dokumentation:
echo   - LAPTOP_TESTING.md      (Detaillierte Anleitung)
echo   - BOT_README.md          (Bot Features)
echo   - RASPBERRY_PI_SETUP.md  (Für Raspberry Pi)
echo.
pause
