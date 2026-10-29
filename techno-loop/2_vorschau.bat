@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
rem 2 Minuten ab Minute 5 - zum Pruefen von Schnitt, Lautsprechern und Titeln
".venv\Scripts\python.exe" -m technoloop bauen projekt.json --vorschau 120 --ab 5:00 %*
pause
