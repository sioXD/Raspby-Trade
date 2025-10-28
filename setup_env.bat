@echo off
REM Environment Setup Script für Windows
REM Erstellt .env Datei automatisch oder interaktiv

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo 🔐 Trading Bot - Full Environment Setup (Windows)
echo ============================================================
echo.

REM Prüfe ob Python installiert
echo [1/4] Prüfe Python Installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nicht gefunden!
    echo Bitte installiere Python 3.8+ von https://python.org
    pause
    exit /b 1
)

echo ✓ Python gefunden
echo.

REM Erstelle Virtual Environment
echo [2/4] Erstelle Virtual Environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual Environment erstellt
) else (
    echo ✓ Virtual Environment bereits vorhanden
)

REM Aktiviere Virtual Environment
echo.
echo [3/4] Aktiviere Virtual Environment und installiere Requirements...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Fehler beim Aktivieren des Virtual Environment
    pause
    exit /b 1
)

python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Fehler beim pip upgrade
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Fehler beim Installieren der Requirements
    pause
    exit /b 1
)

echo ✓ Requirements installiert
echo.

REM Setup .env Datei
echo [4/4] Richte Environment-Variablen auf...
echo.
echo ============================================================
echo Wähle Setup-Option für .env:
echo ============================================================
echo 1) Interaktives Setup (setup_env.py) - EMPFOHLEN
echo 2) Manuell - .env Vorlage kopieren
echo 3) Überspringen
echo.
set /p choice="Deine Wahl (1-3): "

if "%choice%"=="1" (
    echo.
    echo ⏳ Starte interaktives Setup...
    python setup_env.py
    if %errorlevel% equ 0 (
        echo.
        echo ✓ Setup erfolgreich!
    ) else (
        echo ❌ Setup fehlgeschlagen
        pause
        exit /b 1
    )
) else if "%choice%"=="2" (
    echo.
    if exist ".env" (
        echo ⚠ .env Datei existiert bereits!
        set /p overwrite="Überschreiben? (j/N): "
        if not "!overwrite!"=="j" (
            echo Abgebrochen
            exit /b 0
        )
    )
    
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✓ .env erstellt
        echo.
        set /p edit="Öffne .env zum Editieren? (j/N): "
        if "!edit!"=="j" (
            notepad .env
        )
    ) else (
        echo ⚠ .env.example nicht gefunden, überspringe
    )
) else if "%choice%"=="3" (
    echo ✓ .env Setup übersprungen
) else (
    echo ❌ Ungültige Wahl!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Test ob Setup funktioniert:
echo ============================================================
python -c "import src.env_loader; print('✓ Modules OK')" >nul 2>&1

if %errorlevel% equ 0 (
    echo ✓ Alle Module geladen
) else (
    echo ⚠ Warnung: Einige Module konnten nicht geladen werden
)

echo.
echo 🎉 Setup erfolgreich abgeschlossen!
echo.
echo Nächste Schritte:
echo  1. .env Datei bearbeiten mit deine API Keys: .env
echo  2. Tests ausführen:   python test_bot_locally.py
echo  3. Demo starten:      python demo_bot.py
echo  4. Bot starten:       python pi_bot_main.py
echo.
echo HINWEIS: Es wird nur noch .env verwendet, nicht config.yaml!
echo.
pause
