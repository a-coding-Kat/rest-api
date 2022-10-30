# RESTful API, WDB Module Mini-Challenge

The goal of this repository is to implement a RESTful API that offers CRUD access to spotify tracks obtained from [Kaggle](https://www.kaggle.com/datasets/akiboy96/spotify-dataset?resource=download).
It also allows for filtering and pagination of songs by any attribute in the database.

To interact with this server, you can use your own HTTP client, or use the provided Python client.

The tracks are accessible in the **data/** folder in the form of a CSV file. By running **import_data.py** from 
the root of this project you can generate a sqlite3 database file that is later used by the Flask server.

# Getting started

This project requires Python 3.6 or higher.

## Running the server

Clone repository:
```bash
git clone https://github.com/a-coding-Kat/rest-api.git
cd rest-api
```

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

## Running the tests

The server comes with Unit tests you can run. From the root folder of this project:
```bash
python -m unittest test.py
```

## Using the client

Import and initialize the client:

```python
from wdb_rest.client import TrackClient

# Change the URL to the address you are running this server on.
url = "http://127.0.0.1:5000"

client = TrackClient(url)
```

Available methods and which endpoints they access:

| Client method      | Endpoint      | HTTP verb | Description |
| ------------------ | ------------- | --------- | ------------|
| create_track       | Track         | PUT       | Create a new track |
| get_tracks         | TrackList     | GET       | Get list of tracks by some criteria |
| get_track          | Track         | GET       | Get single track by id |
| update_track       | Track         | POST      | Update single track by id. |
| delete_track       | Track         | DELETE    | Delete single track by id. |

More details on these methods are available in the form of doc strings in the client itself.

All methods return a tuple in the format: (**server\_response\_json**, **HTTP return code**). For more information 
on the return JSON and method parameters see the **Rest API** chapter in this document.

# Project dependencies

This project requires Python 3.6 or higher. In addition, the following libraries need to be installed on the machine:

- **Flask** - Application server
- **Flask\_RESTful** - RESTful extension for Flask
- **Flask\_SQLAlchemy** - Object relationship mapping tool for saving and loading Python objects form a database
- **pandas** - Import data from CSV to sqlite
- **requests** - Generate requests from the client

All requirements are added to the **requirements.txt** file.

# Rest API

The rest API offers 2 endpoints for accessing individual tracks and a list of tracks (based on selection criteria).

TODO: WRITE DOWN THE REST INTERFACE.

# Project architecture

The REST api is built on top of Flask and uses **Flask\_RESTful** for creating rest endpoints. The communication with the 
database is done via **Flask\_SQLAlchemy** ORM tool in order to avoid writing SQL queries manually. The database is 
created and populated with data that was scraped from Spotify - songs and their attributes. To communicate with the 
server we offer a Python client which implements access to all available methods.

## import_data.py

This script needs to be run before we start using the REST server, otherwise there will be no database to connect to.
It first creates a new table called **track\_model** in an **sqlite3** database (creates a new file called 
**database.db**).

Table columns:

| Column name      | Type      | Description |
| ---------------- | --------- | ----------- |
| id               | INTEGER   | Primary index of records. This field is auto-incremented by the database. |
| track            | TEXT      | Name of the song. |
| artist           | TEXT      | Name of the artist performing the song. |
| danceability     | REAL      | Danceability score assigned by Spotify. |
| key              | INTEGER   | Key the song is performed in. |
| instrumentalness | REAL      | Instrumentalness score assigned by Spotify. |
| tempo            | REAL      | Tempo of the song. |
| duration_ms      | INTEGER   | Song duration in milliseconds. |
| popularity       | INTEGER   | Song popularity on Spotify. |
| decade           | TEXT      | Decade in which the song was created. |

After the table has been created, the script reads the CSV file with the Spotify data (stored in **data/spotify\_dataset.csv**) 
into a **Pandas Dataframe**. The Dataframe allows for exporting its content into a database with the function **to\_sql**.

## wdb_rest/server.py

RESTful server implementation in Flask. The server uses **SQLAlchemy** to communicate with the sqlite database created 
by the import_data.py script. It declares one model **TrackModel** and 2 Resources (endpoints): 

- **Track** - CRUD access to the data in the **track\_model** table in the database.
- **TrackList** - allows to get a filtered, sorted and paginated list of songs based on some search and sort criteria.

The server validates all create and update requests on the Track resource - 
**all fields in the Track model are mandatory**.

The TrackList endpoint can filter and sort based on the fields in the track_model database. It also offers pagination 
of the results. For string fields it allows for **like** matching: searching for artist "%Lana%" returns all artist 
that have "Lana" somewhere in their name. For numeric fields it allows for exact matching only.

## wdb_rest/client.py

To communicate with the server you can use the provided Python client. It uses the **requests** module  for 
generating HTTP requests and implements all the endpoints the server provides. This is a thin client in the sense 
that no validation or processing happens on the client itself - this is all done on the server. The client just
forwards the user requests and returns the 
server responses.