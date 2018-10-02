@echo off

if NOT EXIST p2p_env (
python -m virtualenv p2p_env)

call p2p_env\Scripts\activate 
pip install -r requirements.txt

python -m pip install Util\python_igraph-0.7.1.post6-cp36-cp36m-win_amd64.whl

cd C:\gurobi751\win64
python setup.py install

cd %~dp0