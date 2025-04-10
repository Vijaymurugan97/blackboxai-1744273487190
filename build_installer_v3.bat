@echo off
echo Building PDF Processor Windows Installer...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher and try again
    pause
    exit /b 1
)

REM Check and create data directory structure if it doesn't exist
if not exist "data" mkdir data
if not exist "data\input" mkdir data\input

REM Install required dependencies
echo Installing required dependencies...
pip install -r requirements.txt

REM Build the installer
echo Building executable with cx_Freeze...
python setup.py build

REM Create the Windows installer
echo Creating Windows installer...
python setup.py bdist_msi

echo.
echo Build complete! The installer can be found in the 'dist' folder.
echo.
pause
