@echo off
setlocal

set TEMP_EXE=%temp%\cpprun_temp.exe
.\mingw\bin\g++ "%~1" -o "%TEMP_EXE%" || exit /b 1
if %errorlevel% neq 0 (
    exit /b %errorlevel%
)

"%TEMP_EXE%" || exit /b 1
if %errorlevel% neq 0 (
    del "%TEMP_EXE%" >nul 2>nul
    exit /b %errorlevel%
)

del "%TEMP_EXE%" >nul 2>nul
exit /b 0