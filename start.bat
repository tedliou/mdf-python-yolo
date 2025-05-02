@echo off
WHERE uv
IF %ERRORLEVEL% NEQ 0 CALL "install.bat"
uv run main.py
