@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
rem Testlauf ohne Maestro: kuenstliche Musik + Testbilder, prueft ffmpeg/NVENC und den ganzen Ablauf
".venv\Scripts\python.exe" -m technoloop demo demo
".venv\Scripts\python.exe" -m technoloop bauen demo\projekt.json
pause
