@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
rem Erzeugt pro Szene mit Girls ein Standbild aus bilder\girl1.png + girl2.png (Maestro: Krea 2 Identity Edit)
rem und speichert es in bilder\keyframes\. Diese Szenen werden danach als nahtlose H3-Loops gerendert.
echo Maestro muss in Pinokio laufen ...
".venv\Scripts\python.exe" -m technoloop keyframes projekt.json %*
pause
