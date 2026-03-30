@echo off
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set TARGET=%~dp0wisprflow.pyw
set SHORTCUT=%STARTUP%\WisprFlow.vbs

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT%"
echo sLinkFile = "%STARTUP%\WisprFlow.vbs" >> "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut("%STARTUP%\WisprFlow.lnk") >> "%SHORTCUT%"
echo oLink.TargetPath = "pythonw.exe" >> "%SHORTCUT%"
echo oLink.Arguments = """%TARGET%""" >> "%SHORTCUT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%SHORTCUT%"
echo oLink.Description = "WisprFlow - Speech to Text" >> "%SHORTCUT%"
echo oLink.Save >> "%SHORTCUT%"

cscript //nologo "%SHORTCUT%"
del "%SHORTCUT%"

echo.
echo WisprFlow will now launch automatically at Windows startup.
pause
