import requests

# If no URL is provided to the client, try to connect to local instance.
default_url = 'http://127.0.0.1:5000/'


class TrackClient:
    """
    Client for communicating with the REST API

    This client enables the user to have CRUD access to the songs stored on the server.
    Additionally, it allows for filtering and sorting the results.
    """

    def __init__(self, url=default_url):
        """
        Create an instance of a client.

        Example:
            from wdb_rest.client import TrackClient
            client = TrackClient('http://127.0.0.1:5000/')

        :param str url: URL of the REST server to connect to. Default value: http://127.0.0.1:5000/
        :return: TrackClient instance
        """
        self.url = url

    def create_track(self, track):
        """
        Create a new track.

        All fields in track dictionary are mandatory to create a track.

        Example:
            track = {
                'track': 'Jealous Kind Of Fella',
                'artist': 'Garland Green',
                'danceability': 0.417,
                'key': 3,
                'instrumentalness': 0.0,
                'tempo': 185.655,
                'duration_ms': 173533.0,
                'popularity': 1,
                'decade': '60s'
            }

            client.create_track(track)

        :param dict track: Dictionary with fields to create a new record.
        :return: tuple(dict of created object, HTTP response code)
        """
        # Passed id=0 is ignored.
        r = requests.put(self.url + 'track/0', track)
        return r.json(), r.status_code

    def get_tracks(self, sort_field='id', sort_order='asc', filter_field=None, filter_value=None):
        """
        Get a list of tracks based on sort and filter criteria.

        #TODO: Comment and describe 'has_next', 'has_prev' etc. fields, what is their purpose.

        String fields: track, artist, decade
        Numeric fields: danceability, key, instrumentalness, tempo, duration_ms, popularity

        You can search on string fields using %like% search. Example: %Happy% will match all tracks that contain "Happy".
        For numerical fields, the match is always exact to the specified number.

        Example:
            client.get_tracks(filter_field='track', filter_value='Beat%',
                              sort_field='danceability', sort_order='desc')

        :param str sort_field: Field to sort by. Default value: 'id'
        :param str sort_order: Ascending or descending order. Valid values: 'asc', 'desc'. Default value: 'asc'
        :param str filter_field: Field to filter by. No filter by default.
        :param str filter_value: Value to filter on. Supported %like% search for string fields.
        :return: tuple(#TODO: Describe the return object., HTTP response code)
        """
        # Prepare parameters for sending to the API.
        params = {'sort_field': sort_field,
                  'sort_order': sort_order,
                  'filter_field': filter_field,
                  'filter_value': filter_value}

        r = requests.get(self.url + 'tracks/', params=params)
        return r.json(), r.status_code

    def get_track(self, track_id):
        """
        Return a single track by id.

        Example:
            client.get_track(15)

        :param int track_id: id of the track to retrieve.
        :return: tuple(dict of requested object, HTTP response code)
        """
        r = requests.get(self.url + 'track/' + str(track_id))
        return r.json(), r.status_code

    def update_track(self, track):
        """
        Update an existing track.

        Pass a dictionary with the updated value. All fields are mandatory.

        String fields: track, artist, decade
        Numeric fields: id, danceability, key, instrumentalness, tempo, duration_ms, popularity

        Example:
            track = client.get_track(44)[0]
            track['danceability'] = track['danceability'] + 0.1
            client.update_track(track)

        :param dict track: Dictionary with fields to update an existing track.
        :return: tuple(dict of created object, HTTP response code)
        """
        r = requests.patch(self.url + 'track/' + str(track['id']), track)
        return r.json(), r.status_code

    def delete_track(self, track_id):
        """
        Delete a single track by id.

        Example:
            client.delete_track(25)

        :param int track_id: id of the track to delete.
        :return: tuple(empty string, HTTP response code)
        """
        r = requests.delete(self.url + 'track/' + str(track_id))
        return r.json(), r.status_code
