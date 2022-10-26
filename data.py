import json

with open("tracks.json") as input_file:
    data = json.load(input_file)

tracks = data.values()

def get_tracks():
    return list(tracks)[:10]

