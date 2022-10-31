from time import time


import pandas as pd
import sqlite3

# Connect to the database.
# Create pandas df.
df = pd.read_csv('data/spotify_dataset.csv')
df = df.reset_index()
df = df.rename(columns={'index': 'id'})

# Connect to database.
conn = sqlite3.connect('database.db')

# Create table needed for import from Pandas dataframe.
create_table_sql = '''
CREATE TABLE "track_model" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "track" TEXT,
  "artist" TEXT,
  "danceability" REAL,
  "key" INTEGER,
  "instrumentalness" REAL,
  "tempo" REAL,
  "duration_ms" INTEGER,
  "popularity" INTEGER,
  "decade" TEXT
)
'''


c = conn.cursor()
# Delete table if already exists.
c.execute("DROP TABLE IF EXISTS track_model")
# Execute create table query.
c.execute(create_table_sql)

# Store pandas df to database. Select only columns of interest.
df = pd.read_csv('data/spotify_dataset.csv')[['track', 'artist', 'danceability', 'key', 'instrumentalness',
                                              'tempo', 'duration_ms', 'popularity', 'decade']]
df.to_sql('track_model', conn, if_exists='append', index=False)



