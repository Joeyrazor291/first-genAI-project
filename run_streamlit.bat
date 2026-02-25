@echo off
REM Restaurant Recommendation Engine - Streamlit Runner (Windows)
REM This script sets up and runs the Streamlit application

echo.
echo 🍽️  Restaurant Recommendation Engine - Streamlit Deployment
echo ===========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements-streamlit.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting Streamlit app...
echo 📱 Open your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
streamlit run streamlit_app.py

pause
