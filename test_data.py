import unittest

from wdb_rest.data import TrackDAO
from wdb_rest.server import db, TrackModel, app


class TestTrackDAO(unittest.TestCase):

    def setUp(self):
        # http://tinyurl.com/2jj8sm6h
        self.app_context = app.app_context()
        self.app_context.push()

        self.track_dao = TrackDAO(db, TrackModel)

        self.track = {
            'track': 'Testing track',
            'artist': 'tester',
            'danceability': 1.0,
            'key': 2,
            'instrumentalness': 3.0,
            'tempo': 4.0,
            'duration_ms': 5.0,
            'popularity': 6.0,
            'decade': '70s'
        }

    def tearDown(self):
        # Look at the tinyurl in the setUp method.
        self.app_context.pop()

    def test_create_track_success(self):
        try:
            track = self.track_dao.create_track(self.track)
        except:
            self.fail("Cannot create track.")

        # Check if our track got an ID from the database.
        self.assertTrue(track.id is not None)

        # Check if all the attributes are the same as the one we added.
        for attribute_name in self.track.keys():
            self.assertEqual(self.track[attribute_name], getattr(track, attribute_name))

    def test_create_track_fail(self):
        # Make copy of original dictionary.
        invalid_track = dict(self.track)
        # Delete one of the attributes.
        del invalid_track['track']

        # The call needs to raise an Exception because we are missing one of the required fields.
        with self.assertRaises(Exception):
            self.track_dao.create_track(invalid_track)

    def test_get_track_success(self):
        # Create track to retrieve.
        created_track = self.track_dao.create_track(self.track)
        created_id = created_track.id
        # Check if we received an id from the create function.
        self.assertTrue(created_id is not None)
        # Use this id to retrieve the object from the database.
        read_track = self.track_dao.get_track_by_id(created_id)

        self.assertEqual(created_track, read_track)

    def test_get_track_fail(self):
        # Track_id 9999999 does not exist.
        invalid_track_id = 9999999

        # This method needs to throw an exception because the track_id is invalid.
        with self.assertRaises(Exception):
            self.track_dao.get_track_by_id(invalid_track_id)

    def test_update_track_success(self):
        modified_track_name = 'Modified track'

        # Create track to modify.
        created_track = self.track_dao.create_track(self.track)
        created_track_id = created_track.id

        # Make copy of original dictionary.
        modified_track_args = dict(self.track)
        modified_track_args['track'] = modified_track_name

        # Update the previously created object.
        updated_track = self.track_dao.update_track_by_id(created_track_id, modified_track_args)

        # Check if the ID of the updated track is the same as of the modified track.
        self.assertEqual(created_track_id, updated_track.id)
        # Check if the value you modified persisted.
        self.assertEqual(updated_track.track, modified_track_name)

    def test_update_track_fail(self):
        # Track_id 9999999 does not exist.
        invalid_track_id = 9999999

        # The update should throw an exception because the track_id does not exist.
        with self.assertRaises(Exception):
            self.track_dao.update_track_by_id(invalid_track_id, self.track)

    def test_delete_track_success(self):
        # Create track to delete.
        created_track = self.track_dao.create_track(self.track)
        created_track_id = created_track.id

        # Delete the newly created track.
        self.track_dao.delete_track_by_id(created_track_id)

        # The track should not be retrievable anymore.
        with self.assertRaises(Exception):
            self.track_dao.get_track_by_id(created_track_id)

    def test_delete_track_fail(self):
        # Track_id 9999999 does not exist.
        invalid_track_id = 9999999

        # The delete should throw an exception because the track_id does not exist.
        with self.assertRaises(Exception):
            self.track_dao.delete_track_by_id(invalid_track_id, self.track)


if __name__ == '__main__':
    unittest.main()
