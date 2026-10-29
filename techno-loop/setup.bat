@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY if exist "%USERPROFILE%\pinokio\bin\miniconda\python.exe" set "PY="%USERPROFILE%\pinokio\bin\miniconda\python.exe""
if not defined PY (
  echo Kein Python gefunden. Installiere Python 3.10+ von python.org ^(Haken bei "Add to PATH"^).
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Erstelle Python-Umgebung ...
  %PY% -m venv .venv || (echo Konnte .venv nicht anlegen & pause & exit /b 1)
)
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt || (echo pip-Installation fehlgeschlagen & pause & exit /b 1)

if not exist musik mkdir musik
if not exist bilder mkdir bilder
if not exist projekt.json copy projekt.example.json projekt.json >nul

where ffmpeg >nul 2>nul || echo Hinweis: ffmpeg nicht im PATH - es wird das mitinstallierte ffmpeg benutzt. Fuer NVENC am besten: winget install Gyan.FFmpeg
echo.
echo Fertig. Jetzt projekt.json anpassen, Songs nach "musik" und Bilder nach "bilder" legen.
pause
