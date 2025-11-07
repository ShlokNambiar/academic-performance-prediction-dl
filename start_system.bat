@echo off
echo ================================================================================
echo ACADEMIC PERFORMANCE PREDICTION SYSTEM - STARTUP SCRIPT
echo ================================================================================
echo.

echo Starting Backend API Server...
echo.
start "API Server" cmd /k "python api_server.py"

echo Waiting for API to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo Starting Frontend Dashboard...
echo.
cd frontend
start "Frontend Dashboard" cmd /k "npm start"
cd ..

echo.
echo ================================================================================
echo SYSTEM STARTUP COMPLETE
echo ================================================================================
echo.
echo Backend API: http://localhost:5000
echo Frontend Dashboard: http://localhost:3000
echo.
echo Two new windows have been opened:
echo   1. API Server (Flask)
echo   2. Frontend Dashboard (React)
echo.
echo To stop the system, close both windows.
echo.
echo Press any key to exit this window...
pause >nul

