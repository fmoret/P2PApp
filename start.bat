@echo off
echo Do you want to update the virtual environment? (y/n) 
set INPUT=
set /P INPUT=%=%

if %INPUT%==n goto packQ

call conda env update -f .\env\AppEnv.yml
goto packQ

:packQ

call activate AppEnv
start /wait "" http://127.0.0.1:8050/
call python P2PMarket_App.py



echo Press "s" to stop...
set INPUT2=
set /P INPUT2=%=%

if %INPUT2%!=s goto closeApp

:closeApp
echo ...closing...