@echo off

call env\Scripts\activate.bat
start /b python app.py

start chrome "http://127.0.0.1:5000"