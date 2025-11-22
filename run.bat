@echo off
REM run_all.bat - Run KAITO Market Tracker and Dashboard on Windows

echo ======================================
echo     KAITO MARKET TRACKER SUITE
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Checking dependencies...
pip install -r requirements.txt -q

REM Menu
echo.
echo What would you like to do?
echo 1) Run market analysis
echo 2) Launch dashboard
echo 3) Run analysis then launch dashboard
echo 4) Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting market analysis...
    python main.py %*
) else if "%choice%"=="2" (
    echo.
    python run_dashboard.py
) else if "%choice%"=="3" (
    echo.
    echo Starting market analysis...
    python main.py %*
    if %errorlevel% equ 0 (
        echo.
        echo Analysis complete! Launching dashboard...
        timeout /t 2 /nobreak > nul
        python run_dashboard.py
    ) else (
        echo Analysis failed. Dashboard not launched.
    )
) else if "%choice%"=="4" (
    echo Exiting...
) else (
    echo Invalid choice. Exiting...
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo Done!
pause