pushd venv\Scripts
call activate.bat
popd
pip install -r requirements.txt
pushd  apache-tinkerpop-gremlin-server-3.4.11\bin
start gremlin-server.bat
popd
python run.py
