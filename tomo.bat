call activate venv
call /apache-tinkerpop-gremlin-server-3.4.11-bin/apache-tinkerpop-gremlin-server-3.4.11/bin/gremlin-server.bat
pip install -r requirements.txt
python run.py
