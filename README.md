# RESTful API, WDB Module Mini-Challenge

The goal of this repository is to implement a RESTful API that offers CRUD access to Spotify tracks obtained from [Kaggle](https://www.kaggle.com/datasets/akiboy96/spotify-dataset?resource=download).
It also allows for filtering and pagination of songs by any attribute in the database.

To interact with this server, you can use your own HTTP client, or use the provided Python client.

The tracks are accessible in the **data/** folder in the form of a CSV file. By running **import_data.py** from 
the root of this project you can generate a sqlite3 database file that is later used by the Flask server.

# Getting started

This project requires Python 3.6 or higher.

Clone repository:
```bash
git clone https://github.com/a-coding-Kat/rest-api.git
cd rest-api
```

## Running the server in Docker

To build and run the container execute from the root of this project:
```bash
sh build_docker.sh
sh run_docker.sh
```

Alternatively, if you do not have bash, you can execute the build and run command manually:
```bash
docker build -t wdb_rest .
docker run -it -p 5000:5000 wdb_rest
```

The web service will be accessible on the URL **http://127.0.0.1:5000**.

## Running the server manually

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

Before running the tests you must initialize the database by running import_data.py.
The tests will modify the database. Rerun import_data.py before starting the server.
To use the tests on a test database, the database connection string in server.py needs to be adjusted to go to "database-test.db" instead of database.db. When starting the server, the test database will then be used. We tried to implement an automatic connection to the test database while testing, but this didn't work and it is on the TODO-list.

### Unit tests

From the root folder of this project:
```bash
python -m unittest test_data.py
```

### Integration tests

Before running integration tests you must run the server. You can do this via docker or with the instructions above.
Integration tests also modify the database, so afterwards re-run import_data.py.

From the root folder of this project:
```bash
python -m unittest test_api.py
```

## Using the client

Import and initialize the client:

```python
from wdb_rest.client import TrackClient

# Change the URL to the address you are running this server on.
url = "http://127.0.0.1:5000/api/"

client = TrackClient(url)
```

Available methods and which endpoints they access:

| Client method      | Endpoint      | HTTP verb | Description                          |
| ------------------ | ------------- | --------- |--------------------------------------|
| create_track       | Track         | PUT       | Create a new track.                  |
| get_tracks         | TrackList     | GET       | Get list of tracks by some criteria. |
| get_track          | Track         | GET       | Get single track by id.              |
| update_track       | Track         | POST      | Update single track by id.           |
| delete_track       | Track         | DELETE    | Delete single track by id.           |

More details on these methods are available in the form of doc strings in the client itself.

All methods return a tuple in the format: (**server\_response\_json**, **HTTP return code**). For more information 
on the return JSON and method parameters see the **REST API** chapter in this document.

# Project dependencies

The following libraries need to be installed on the machine:

- **Flask** - Application server
- **Flask\_RESTful** - RESTful extension for Flask
- **Flask\_SQLAlchemy** - Object relationship mapping tool for saving and loading Python objects form a database
- **pandas** - Import data from CSV to sqlite
- **requests** - Generate requests from the client

All requirements are added to the **requirements.txt** file.

# REST API

The REST API offers 3 endpoints for accessing individual tracks and a list of tracks (based on the selection criteria).
* **TrackList endpoint** `/api/tracks/`: Get a list of songs based on some criteria
    - **GET** `/api/tracks/`: Return the requested list of Tracks
    
        This endpoints supports 5 URL parameters:
        - page (default = 1) - which page of the paginated result you want to read.
        - sort_field (default = 'id) - by which field to order the result.
        - sort_order (default = 'asc') - in which direction ('asc' or 'desc') to order the results.
        - filter_field (optional) - field on which to filter.
        - filter_value (optional) - field value on which to filter.
        
        This endpoints always returns results paginated with page_size = 10. The **page** URL parameters defines which 
        page would you like to receive back. If not specified otherwise, the sorting is always done in ascending order 
        on the id field. The filtering is by default disabled, but if you specify the **filter_field** and 
        **filter_value** your results will be filtered accordingly:
        - If the filter_field is a string, the service supports exact matches as well as '%LIKE%' SQL style matches.
        - If the filter_field is a number, we support only exact match.
        
        TODO: DESCRIBE THIS ENTIRE RETURN FORMAT.
    
        Example:
        ```bash
        # Retrieve the first page of songs whose artist contains the string "%Lana%", sorted by id in ascending order.
        curl -s -X GET http://localhost:5000/api/tracks/?page=1&sort_field=id&sort_order=asc&filter_field=artist&filter_value=%Lana%
        ```
        Positive response (HTTP code 200):
        ```json
        {
            "page": 1,
            "has_next": true,
            "has_prev": false,
            "tracks_iter": [1,2,3,4,5,null,4109,4110],
            "next_num": 2,
            "items": [],
            "prev_num": null
        }
        ```

* **Track endpoint** `/api/track/<int:track_id>`: CRUD access to Track records in database.
    - **GET** `/api/track/<int:track_id>` - retrieve single Track by id.

        Get returns you the requested Track if successful and a message telling you what is wrong otherwise.
    
        Example:
        ```bash
        # Retrieve track with id=1
        curl -s -X GET http://localhost:5000/api/track/1
        ```
        Positive response (HTTP code 200):
        ```json
        {
            "id": 1,
            "track": "Jealous Kind Of Fella",
            "artist": "Garland Green",
            "danceability": 0.417,
            "key": 3,
            "instrumentalness": 0.0,
            "tempo": 185.655,
            "duration_ms": 173533.0,
            "popularity": 1,
            "decade": "60s"
        }
        ```
        Negative response (HTTP code 500):
        ```json
        {
          "msg": "Cannot get track, track_id does not exist."
        }
        ```
    - **PUT** `/api/track/<int:track_id>` - Create new Track record
    
        Creates a new Track. All fields are mandatory. Check the chapter **import\_data.py** below for more details
        on the attributes and their types. You must specify all attributes in the database except **id**, because 
        the database will assign it to the new Track.
        
        If successful you will get the newly created Track back, otherwise you will get a message telling you what is 
        wrong.
    
        Example:
        ```bash
        # Create a new track. Note: you must pass 0 as the track_id in the URL when doing this request.
        curl -s -X PUT http://localhost:5000/api/track/0 -H "Content-Type: application/json" -d '
        {
            "track": "Jealous Kind Of Fella",
            "artist": "Garland Green",
            "danceability": 0.417,
            "key": 3,
            "instrumentalness": 0.0,
            "tempo": 185.655,
            "duration_ms": 173533.0,
            "popularity": 1,
            "decade": "60s"
        }'
        ```
        Positive response (HTTP code 201):
        ```json
        {
            "id": 41100,
            "track": "Jealous Kind Of Fella",
            "artist": "Garland Green",
            "danceability": 0.417,
            "key": 3,
            "instrumentalness": 0.0,
            "tempo": 185.655,
            "duration_ms": 173533.0,
            "popularity": 1,
            "decade": "60s"
        }
        ```
        Negative response (HTTP code 500) (example if request was missing "decade" attribute):
        ```json
         {"message": { "decade": "Decade is required." }}
        ```
    - **PATCH** `/api/track/<int:track_id>` - Update existing track by id
    
        Updates an existing Track. All fields are mandatory. Check the chapter **import\_data.py** below for more details
        on the attributes and their types.
        
        If successful you will get the newly updated Track back, otherwise you will get a message telling you what is 
        wrong.
    
        Example:
        ```bash
        # Update track with id=1
        curl -s -X PATCH http://localhost:5000/api/track/1 -H "Content-Type: application/json" -d '
        {
            "id": 1,
            "track": "Jealous Kind Of Fella",
            "artist": "Garland Green",
            "danceability": 0.417,
            "key": 3,
            "instrumentalness": 0.0,
            "tempo": 185.655,
            "duration_ms": 173533.0,
            "popularity": 1,
            "decade": "60s"
        }'
        ```
        Postive response (HTTP code 200):
        ```json
        {
            "id": 1,
            "track": "Jealous Kind Of Fella",
            "artist": "Garland Green",
            "danceability": 0.417,
            "key": 3,
            "instrumentalness": 0.0,
            "tempo": 185.655,
            "duration_ms": 173533.0,
            "popularity": 1,
            "decade": "60s"
        }
        ```
        Negative response (HTTP code 500):
        ```json
        {
          "msg": "Cannot update track, track_id does not exist."
        }
        ```
    - **DELETE** `/api/track/<int:track_id>` - Delete existing track by id
    
        Delete the requested Track. If successful an empty JSON will be returned, otherwise a message telling you 
        what is wrong.
    
        Example:
        ```bash
        # Delete track with id=1
        curl -s -X DELETE http://localhost:5000/api/track/1
        ```
        Positive response (HTTP code 200):
        ```json
        {}
        ```
        Negative response (HTTP code 500):
        ```json
        {
          "msg": "Cannot delete track, track_id = 1 does not exist."
        }
        ```

* **Track endpoint** `/api/recommendation/<int:track_id>/<int:how_many_recommendations>`: Get a list of recommendations for a song.
    - **GET** `/api/track/<int:track_id>/<int:how_many_recommendations>'` - Return a selected list of recommendations based on a song.

        Get returns you a list of tracks similar to a track based on its ID. The similarity is calculated using cosine similarity and uses the following track attributes for recommendation:
        
        - danceability
        - key
        - instrumentalness
        - tempo
        - duration_ms
        - popularity
        - decade

        This endpoint supports the following parameters:
        how_many_recommendations (default = 10) - How many recommendations should the api return. Minimum is 1, maximum is 100.
        
        In a further step, there will be the possibility to retrieve recommendations by weighing the attributes above differently. For example [10, 1, 1, 1, 1, 1, 1] would mean recommending songs mostly based on their "danceability" similarity. 
    
        Example:
        ```bash
        # Retrieve recommendations for track with id=1
        curl -s -X GET http://localhost:5000/api/recommendation/1/?how_many_recommendations=10
        ```
        Positive response (HTTP code 200):
        ```json
        [
            {
                "id":3,
                "track":"Melody Twist",
                "artist":"Lord Melody",
                "danceability":0.657,
                "decade":"60s",
                "duration_ms":223960.0,
                "instrumentalness":4.42e-06,
                "key":5,
                "popularity":0,
                "tempo":115.94
            },
            {
                "id":1647,
                "track":"Who Is Gonna Love Me?",
                "artist":"Dionne Warwick",
                "danceability":0.353,
                "decade":"60s",
                "duration_ms":192573.0,
                "instrumentalness":0.0,
                "key":0,"popularity":1,
                "tempo":94.655
            }
        ]
        ```
        Negative response (HTTP code 500):
        ```json
        {
          "msg": "Invalid track id or track not found."
        }
        ```

# Project architecture

The REST api is built on top of Flask and uses **Flask\_RESTful** for creating rest endpoints. The communication with the 
database is done via **Flask\_SQLAlchemy** ORM tool in order to avoid writing SQL queries manually. The database is 
created and populated with Spotify songs and their attributes. To communicate with the server we offer a Python client 
which implements access to all available methods.

## import_data.py

This script needs to be run before we start using the REST server, otherwise there will be no database to connect to.
It first creates a new table called **track\_model** in an **sqlite3** database (creates a new file called 
**database.db**).

Table columns:

| Column name      | Type      | Description                                                               |
| ---------------- | --------- |---------------------------------------------------------------------------|
| id               | INTEGER   | Primary index of records. This field is auto-incremented by the database. |
| track            | TEXT      | Name of the track.                                                        |
| artist           | TEXT      | Name of the artist performing the track.                                  |
| danceability     | REAL      | Danceability score assigned by Spotify.                                   |
| key              | INTEGER   | Key the track is performed in.                                            |
| instrumentalness | REAL      | Instrumentalness score assigned by Spotify.                               |
| tempo            | REAL      | Tempo of the track.                                                       |
| duration_ms      | INTEGER   | Track duration in milliseconds.                                           |
| popularity       | INTEGER   | Track popularity on Spotify.                                              |
| decade           | TEXT      | Decade in which the track was created.                                    |

After the table has been created, the script reads the CSV file with the Spotify data (stored in **data/spotify\_dataset.csv**) 
into a **Pandas Dataframe**. The Dataframe allows for exporting its content into a database with the function **to\_sql**. A copy of the database is created for testing. It holds the same but with the suffix "-test". 

## wdb_rest/server.py

RESTful server implementation in Flask. The server uses **SQLAlchemy** to communicate with the sqlite database created 
by the import_data.py script. It declares one model **TrackModel** and 2 Resources (endpoints): 

- **Track** - CRUD access to the data in the **track\_model** table in the database.
- **TrackList** - allows to get a filtered, sorted and paginated list of songs based on some search and sorting criteria.

The server validates all create and update requests on the Track resource - 
**all fields in the Track model are mandatory**.

The TrackList endpoint can filter and sort based on the fields in the track_model database. It also offers pagination 
of the results. For string fields it allows for **like** matching: searching for artist "%Lana%" returns all artist 
that have "Lana" somewhere in their name. For numeric fields it allows for exact matching only.

## wdb_rest/data.py

Data access object that communicates with the database and implements all the data operations needed by server.py.
With this file we separate the API definition (in server.py) and the database access code (in data.py), making it 
easier to change the data storage if needed.

## wdb_rest/client.py

To communicate with the server you can use the provided Python client. It uses the **requests** module  for 
generating HTTP requests and implements all the endpoints the server provides. This is a thin client in the sense 
that no validation or processing happens on the client itself - this is all done on the server. The client just
forwards the user requests and returns the server responses.
