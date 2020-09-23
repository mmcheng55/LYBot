@echo off
:startup
E:\python\python.exe E:\Projects\LightYear\main.py
echo.
ECHO Server will re-start *automatically* in less than 30 seconds...
CHOICE /M:"Restart now (Y) or Exit (N)" /T:30 /D:Y
IF %ERRORLEVEL% GEQ 2 (
	ECHO INFO: Server manually stopped before auto-restart 1>>  "%~dp0logs\serverstart.log" 2>&1
	GOTO end
) ELSE ( 
	GOTO startup
)

:end
