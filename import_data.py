import pandas as pd
import sqlite3

# Create pandas df.
df = pd.read_csv('data/spotify_dataset.csv')
df = df.reset_index()
df = df.rename(columns={'index': 'id'})

# Connect to database.
conn = sqlite3.connect('database.db')

# Store pandas df to database.
df.to_sql('track_model', conn, if_exists='replace', index=False)

