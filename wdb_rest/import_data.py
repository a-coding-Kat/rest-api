import json
from wdb_rest.server import TrackModel

with open("../data/tracks.json") as input_file:
    data = json.load(input_file)

tracks = list(data.values())

# Iterate over nested dictionary to extract track information.
for artist_tracks in tracks:
    for track_id, track in artist_tracks.items():
        print(track_id, track)
