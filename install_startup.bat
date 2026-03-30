@echo off
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set PYTHONW=%~dp0.venv\Scripts\pythonw.exe
set TARGET=%~dp0wisprflow.pyw
set SHORTCUT=%STARTUP%\sPEAK.vbs

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut("%STARTUP%\sPEAK.lnk") >> "%SHORTCUT%"
echo oLink.TargetPath = "%PYTHONW%" >> "%SHORTCUT%"
echo oLink.Arguments = """%TARGET%""" >> "%SHORTCUT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%SHORTCUT%"
echo oLink.Description = "sPEAK - Speech to Text" >> "%SHORTCUT%"
echo oLink.Save >> "%SHORTCUT%"

cscript //nologo "%SHORTCUT%"
del "%SHORTCUT%"

echo.
echo sPEAK will now launch automatically at Windows startup.
pause
