@echo off
REM Launch the rFactor 2 Setup Program from its own directory.
cd /d "%~dp0"
python rf2_setup.py
if errorlevel 1 (
    echo.
    echo The program exited with an error. Press any key to close.
    pause >nul
)
