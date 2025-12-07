@echo off
python -m venv venv
.\venv\scripts\activate
pip install -r requirements.txt
echo WEBSERVER_SECRET="" > ".env"
echo Finished initiating workspace!
pause