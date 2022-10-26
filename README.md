# RESTful API for WDB Module Minichallenge

Create environment:
```bash
python -m venv wdb
# On Windows: .\wdb\Scripts\activate
source wdb/bin/activate
pip install -r requirements.txt
```

To create the database, execute the import_data.py from the root of the project:
```bash
python import_data.py
```

Start the REST server from the root of the project.
```bash
python wdb_rest/server.py
```