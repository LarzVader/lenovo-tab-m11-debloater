@echo off
rem Lenovo Tab M11 Debloater - start on Windows / Start unter Windows
setlocal
cd /d "%~dp0"
chcp 65001 >nul

set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY (
    python --version >nul 2>&1 && set "PY=python"
)

if not defined PY (
    echo.
    echo Python 3 was not found. / Python 3 wurde nicht gefunden.
    echo.
    echo Install it with this command / Installiere es mit diesem Befehl:
    echo     winget install -e --id Python.Python.3.13
    echo or from / oder von: https://www.python.org/downloads/
    echo.
    echo Then start this file again. / Dann starte diese Datei erneut.
    echo.
    pause
    exit /b 1
)

%PY% "%~dp0m11_debloater.py" %*
echo.
pause
