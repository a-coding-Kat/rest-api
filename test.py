from wdb_rest.client import TrackClient
client = TrackClient()
track, status_code = client.get_track(42)
print(track)

