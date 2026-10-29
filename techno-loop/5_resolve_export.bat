@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
rem Schnittliste (EDL) + Overlay (Lautsprecher/Titel mit Transparenz) + Musik-WAV fuer DaVinci Resolve
".venv\Scripts\python.exe" -m technoloop resolve projekt.json %*
pause
