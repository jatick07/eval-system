@echo off


echo Installing Compilers and Interpreters...
echo.

echo Installing Node.js Portable...

curl -s -o node_index.json https://nodejs.org/dist/index.json
for /f "tokens=2 delims=:," %%a in ('findstr /i /c:"version" node_index.json ^| findstr /v /c:"nightly" ^| findstr /v /c:"test" ^| findstr /i /c:"lts"') do (
    set ver=%%a
    goto :gotVersion
)

:gotVersion
set ver=%ver:"=%
set ver=%ver:v=%
del node_index.json >nul 2>&1

set NODEZIP=node-v%ver%-win-x64.zip
set URL=https://nodejs.org/dist/v%ver%/%NODEZIP%
echo Downloading %NODEZIP%...
curl -L -o "%NODEZIP%" "%URL%"

echo Extracting...
rmdir /s /q node 2>nul
mkdir node
tar -xf "%NODEZIP%" -C node --strip-components=1
del "%NODEZIP%"

echo Installed Node.js Standalone v%ver%
echo.
echo.



echo Installing MinGW-w64...

set MINGWZIP=mingw.zip
echo Downloading %MINGWZIP%...
curl -L -o "%MINGWZIP%" https://github.com/brechtsanders/winlibs_mingw/releases/download/15.2.0posix-13.0.0-msvcrt-r1/winlibs-x86_64-posix-seh-gcc-15.2.0-mingw-w64msvcrt-13.0.0-r1.zip

echo Extracting...
mkdir mingw
tar -xf "%MINGWZIP%" -C mingw --strip-components=1
del "%MINGWZIP%"

echo Installed MinGW-w64
echo.
echo.



echo Intitializing python virtual environment...
python -m venv venv
call .\venv\Scripts\activate.bat

echo Installing Requirements...
pip install -r requirements.txt

echo WEBSERVER_SECRET="" > ".env"
echo.
echo.
echo Finished initiating workspace!

pause