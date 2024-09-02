@echo off
:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    :: The script is already running with admin privileges
    echo Running as Administrator
) else (
    :: Request elevation
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Existing script content
call "D:\Raihan Parfum\env\Scripts\activate.bat"
start /b python "D:\Raihan Parfum\app.py"
start "" "C:\Users\LENOVO\Desktop\Google Chrome.lnk" "http://127.0.0.1:5000"