@echo off

call "D:\Raihan Parfum\env\Scripts\activate.bat"
start /b python "D:\Raihan Parfum\app.py"

start "" "chrome.exe" "http://127.0.0.1:5000"