@echo off
setlocal

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Pull the latest changes from the remote repository
cd /d "%SCRIPT_DIR%"
git pull

REM Copy new files to the current folder
for /r "%SCRIPT_DIR%utilities" %%i in (*) do (
    copy /y "%%i" "%SCRIPT_DIR%"
)

REM Display a message indicating successful update
echo Update complete!
