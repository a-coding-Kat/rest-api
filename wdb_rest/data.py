import json

from sqlalchemy import literal_column

from wdb_rest.alchemy_encoder import AlchemyEncoder


class TrackDAO:
    """
    Data access object for reading Tracks from the database.
    """

    def __init__(self, db, track_model):
        """
        Initialize object.

        :param db: SQLAlcemy instance of database.
        :param track_model: Model to access.
        """
        self.db = db
        self.track_model = track_model

    def get_tracks_list(self, filter_field=None, filter_value=None, sort_field='id', sort_order='asc', page=1):
        """
        Get a list of tracks based on sort and filter criteria.

        String fields: track, artist, decade
        Numeric fields: danceability, key, instrumentalness, tempo, duration_ms, popularity

        You can search on string fields using %like% search. Example: %Happy% will match all tracks that contain "Happy".
        For numerical fields, the match is always exact to the sepcified number.

        Example:
            track_dao.get_tracks_list(filter_field='track', filter_value='Beat%',
                                      sort_field='danceability', sort_order='desc')

        :param str filter_field: Field to filter by. No filter by default.
        :param str filter_value: Value to filter on. Supported %like% search for string fields.
        :param str sort_field: Field to sort by. Default value: 'id'
        :param str sort_order: Ascending or descending order. Valid values: 'asc', 'desc'. Default value: 'asc'

        :return: TODO: Describe the return object.
        """

        # Create query object for track_model.
        query = self.track_model.query

        # Sort by the user-provided column.
        if getattr(self.track_model, sort_field, None) is None:
            raise Exception(f'Provided sort_field {sort_field} does not exist.')

        # Check if sorting order is valid.
        if sort_order == 'asc':
            query = query.order_by(getattr(self.track_model, sort_field))
        elif sort_order == 'desc':
            query = query.order_by(getattr(self.track_model, sort_field).desc())
        else:
            raise Exception(f'Provided sort_order {sort_order} is invalid. Use asc or desc.')

        # Check if the filter fields were provided and are valid.
        if filter_field is not None and filter_value is not None:
            if getattr(self.track_model, filter_field, None) is None:
                raise Exception(f'Provided filter field {filter_field} does not exist.')

            # Track and artist support like search.
            if filter_field in ['track', 'artist']:
                query = query.filter(literal_column(filter_field).like(filter_value))
            # Other fields exact match only.
            else:
                query = query.filter(getattr(self.track_model, filter_field) == filter_value)

        # Request pagination from the database.
        tracks = query.paginate(page=page, per_page=10)

        # Iterate instead of returning dictionary at once.
        pages_nums = []
        for page_num in tracks.iter_pages():
            pages_nums.append(page_num)

        # Create response object.
        items = json.dumps(tracks.items, cls=AlchemyEncoder)
        package = dict(page=tracks.page, has_next=tracks.has_next, has_prev=tracks.has_prev,
                       tracks_iter=pages_nums, next_num=tracks.next_num, items=items, prev_num=tracks.prev_num)

        return package

    def create_track(self, args):
        """
        Create a new track.

        All fields in track dictionary are mandatory to create a track.

        Example:
            args = {
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

            track_dao.create_track(args)

        :param dict args: Dictionary with fields to create a new record.
        :return: created object.
        """

        track = self.track_model(**args)
        self.db.session.add(track)
        # Flushing the transaction to get an id.
        self.db.session.flush()

        # Store the track_id.
        track_id = track.id

        # Commit transaction to create the object.
        self.db.session.commit()

        # Load track from the database.
        track = self.track_model.query.filter_by(id=track_id).first()

        return track

    def get_track_by_id(self, track_id):
        """
        Return a single track by id.

        Example:
            track_dao.get_track(15)

        :param int track_id: id of the track to retrieve.
        :return: requested object
        """
        track = self.track_model.query.filter_by(id=track_id).first()

        if not track:
            raise Exception('Cannot get track, track_id does not exist.')

        return track

    def update_track_by_id(self, track_id, args):
        """
        Update an existing track.

        Pass a dictionary with the updated value. All fields are mandatory.

        String fields: track, artist, decade
        Numeric fields: id, danceability, key, instrumentalness, tempo, duration_ms, popularity

        Example:
            track = track_dao.get_track(44)[0]
            track['danceability'] = track['danceability'] + 0.1
            track_dao.update_track_by_id(track['id'], track)

        :param int track_id: Id of the track to update
        :param dict args: Dictionary with fields to update an existing track.
        :return: updated object
        """
        track = self.track_model.query.filter_by(id=track_id).first()
        if not track:
            raise Exception('Cannot update track, track_id does not exist.')

        self.track_model.query.filter_by(id=track_id).update(args)
        self.db.session.commit()

        track = self.track_model.query.filter_by(id=track_id).first()

        return track

    def delete_track_by_id(self, track_id):
        """
        Delete a single track by id.

        Example:
            track_dao.delete_track(25)

        :param int track_id: id of the track to delete.
        :return: None
        """
        track = self.track_model.query.filter_by(id=track_id).first()

        if not track:
            raise Exception(f'Cannot delete track, track_id = {track_id} does not exist.')

        self.db.session.delete(track)
        self.db.session.commit()
