@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
echo Maestro muss in Pinokio laufen. Szenen werden nacheinander mit MiniMax H3 gerendert ...
".venv\Scripts\python.exe" -m technoloop szenen projekt.json %*
pause
