
@echo off
title Run as Administrator Prompt
color 0C

echo.
echo ----------------------------------------------
echo This script needs administrator privileges.
echo Please run it as an administrator.
echo ----------------------------------------------
echo.

:: Check for administrative rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" && (
    echo Administrative privileges detected. Proceeding...
    goto :main
) || (
    echo Unable to detect administrative privileges.
    echo Please right-click and select "Run as Administrator".
    pause
    exit /B
)

:main
color 07
echo.
echo Script is now running with administrator privileges.
echo.

setlocal enabledelayedexpansion

set "scriptPath=%~dp0"

echo Adding folder to PATH: !scriptPath!
setx /M path !scriptPath!


endlocal

pause
exit /B
