@echo off
echo Do you want to update repository? (y/n) 
set INPUT=
set /P INPUT=%=%

if %INPUT%==n goto packQ

cd C:\Program Files\TortoiseSVN\bin\
START /wait TortoiseProc.exe /command:update /path:"C:\SISMA\" /closeonend:0

:packQ

echo Do you want to update the packages? (y/n) 
set INPUT2=
set /P INPUT2=%=%

if %INPUT2%==n goto launch

conda env update -f C:\SISMA\trunk\envs\sismaEnv.yml
goto launch

:launch
	cd C:\Users
	call activate sisma
	spyder