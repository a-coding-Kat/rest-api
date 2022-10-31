import unittest
import json
from wdb_rest.server import app
import unittest
from wdb_rest.client import TrackClient

class SignupTest(unittest.TestCase):

    def setUp(self):
        print("Starting Tests")
        self.client = TrackClient()

    def test_get_track(self):

        track, status_code = self.client.get_track(42)
        self.assertEqual(str, type(track['artist']))
        self.assertEqual(200, status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        pass