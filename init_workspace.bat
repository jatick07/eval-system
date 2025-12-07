@echo off
python -m venv venv
echo Intitialized the python virtual environment

call .\venv\Scripts\activate.bat
echo Installing Requirements...
pip install -r requirements.txt

echo WEBSERVER_SECRET="" > ".env"
echo.
echo.
echo Finished initiating workspace!

pause