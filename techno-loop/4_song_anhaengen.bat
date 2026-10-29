@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (echo Bitte zuerst setup.bat ausfuehren. & pause & exit /b 1)
rem Zeigt alle WAV/MP3 aus Downloads, C:\Download\suno, F:\Pinokio Projekt ... und haengt die gewaehlten hinten an.
rem Direkt per Name:  4_song_anhaengen.bat --suche "Songname"
".venv\Scripts\python.exe" -m technoloop song-dazu projekt.json %*
pause
