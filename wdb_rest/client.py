import requests

default_url = 'http://127.0.0.1:5000/'


class TrackClient:
    def __init__(self, url=default_url):
        self.url = url

    def create_track(self, track):
        r = requests.put(self.url + 'track/0', track)
        return r.json(), r.status_code

    # Get a list of tracks.
    def get_tracks(self, sort_field='id', sort_order='asc', filter_field=None, filter_value=None):
        params = {'sort_field': sort_field,
                  'sort_order': sort_order,
                  'filter_filed': filter_field,
                  'filter_value': filter_value}

        r = requests.get(self.url + 'tracks/', params=params)
        return r.json(), r.status_code

    def get_track(self, track_id):
        r = requests.get(self.url + 'track/' + str(track_id))
        return r.json(), r.status_code

    def update_track(self, track):
        r = requests.patch(self.url + 'track/' + str(track['track_id']), track)
        return r.json(), r.status_code

    def delete_track(self, track_id):
        r = requests.delete(self.url + 'track/' + str(track_id))
        return r.json(), r.status_code
