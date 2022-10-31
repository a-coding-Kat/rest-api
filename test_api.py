import json
from cmath import e
import unittest
from wdb_rest.client import TrackClient


class IntegrationTests(unittest.TestCase):

    def setUp(self):
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

        self.client = TrackClient()

        #invalid track id
        self.invalid_track_id = 99999999

    def test_create_track_success(self):

        track, response_code = self.client.create_track(self.track)

        # Check if our track got an ID from the database.
        self.assertTrue(track['id'] is not None)

        # Check if the return code is correct
        self.assertEqual(response_code, 201)

        # Check if all the attributes are the same as the one we added.
        for attribute_name in self.track.keys():
            self.assertEqual(self.track[attribute_name], track[attribute_name])

    def test_create_track_fail(self):
        # Make copy of original dictionary.
        invalid_track = dict(self.track)
        # Delete one of the attributes.
        del invalid_track['track']

        # The call needs to raise an Exception because we are missing one of the required fields.
        read_track, response_code = self.client.create_track(invalid_track)

        # Check if we got a 400 code.
        self.assertEqual(response_code, 400)

        # Check if the error message is as expected.
        self.assertDictEqual(read_track['message'], {'track': 'Name of the track is required.'})


    def test_get_track_success(self):
        # Create track to retrieve.
        created_track, response_code = self.client.create_track(self.track)
        # Check if the response code is correct.
        self.assertEqual(response_code, 201)

        created_id = created_track['id']
        # Check if we received an id from the create function.
        self.assertTrue(created_id is not None)
        # Use this id to retrieve the object from the database.
        read_track, response_code = self.client.get_track(created_id)
        # Check response code
        self.assertEqual(response_code, 200)
        # Compare created and read track.
        self.assertEqual(created_track, read_track)

    def test_get_track_fail(self):
        # This method needs to throw an exception because the track_id is invalid.
        response, return_code = self.client.get_track(self.invalid_track_id)

        # Check if we got a 500 code.
        self.assertEqual(return_code, 500)
        # Check the return message.
        self.assertEqual(response['msg'], 'Cannot get track, track_id does not exist.')

    def test_update_track_success(self):
        modified_track_name = 'Modified track'

        # Create track to modify.
        created_track, response_code = self.client.create_track(self.track)
        # Check if the response code is correct.
        self.assertEqual(response_code, 201)

        # Make copy of original dictionary.
        created_track['track'] = modified_track_name

        # Update the previously created object.
        updated_track, response_code = self.client.update_track(created_track)
        # Check if the response code is correct.
        self.assertEqual(response_code, 200)

        # Check if the value you modified persisted.
        self.assertDictEqual(created_track, updated_track)

    def test_update_track_fail(self):

        # Make copy of original dictionary.
        invalid_track = dict(self.track)
        invalid_track['id'] = self.invalid_track_id

        # The update should throw an exception because the track_id does not exist.
        response, response_code = self.client.update_track(invalid_track)

        # Check if we get an error
        self.assertEqual(response_code, 500)

        # Check if we got the expected message
        self.assertEqual(response['msg'], 'Cannot update track, track_id does not exist.')

    def test_delete_track_success(self):
        # Create track to retrieve.
        created_track, response_code = self.client.create_track(self.track)
        # Check if the response code is correct.
        self.assertEqual(response_code, 201)

        created_track_id = created_track['id']

        # Delete the newly created track.
        response, response_code = self.client.delete_track(created_track_id)

        # Check if we got a correct response code.
        self.assertEqual(response_code, 200)

        # Check if the return object is empty.
        self.assertDictEqual(response, {})

        # The track should not be retrievable anymore.
        response, response_code = self.client.get_track(created_track_id)

        # Check if we get an error
        self.assertEqual(response_code, 500)

        # Check if we got the expected message
        self.assertEqual(response['msg'], 'Cannot get track, track_id does not exist.')

    def test_delete_track_fail(self):

        # The delete should throw an exception because the track_id does not exist.
        response, response_code = self.client.delete_track(self.invalid_track_id)

        # Check if we get an error
        self.assertEqual(response_code, 500)
        self.client = TrackClient()
        # Check if we got the expected message
        self.assertEqual(response['msg'], f'Cannot delete track, track_id = {self.invalid_track_id} does not exist.')

    def test_get_recommendations_success(self):

        response, status_code = self.client.recommend_tracks(42, 12)
        self.assertEqual(list, type(response))

        #check if length of recommendation matches request
        self.assertEqual(12, len(response))
        self.assertEqual(200, status_code)

    def test_get_recommendations_fail(self):


        # Check if an invalid track id returns correct error code
        response, status_code = self.client.recommend_tracks(self.invalid_track_id, 1)
        self.assertEqual(500, status_code)
        self.assertEqual(response['msg'], 'Invalid track id or track not found.')

    def test_get_all_tracks_sorting(self):

        #check if sorting asc/desc yields different search results based on sort_field
        tracks_asc, status_code = self.client.get_tracks(sort_order = "asc", sort_field = "tempo")
        tracks_desc, status_code = self.client.get_tracks(sort_order = "desc", sort_field = "tempo")
        first_item_asc = json.loads(tracks_asc["items"])[0]
        first_item_desc = json.loads(tracks_desc["items"])[0]
        self.assertGreater(first_item_desc["tempo"], first_item_asc["tempo"])
