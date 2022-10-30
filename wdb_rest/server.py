import json
from flask import Flask, send_from_directory, Markup, render_template, request
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
import requests

from wdb_rest.data import TrackDAO

# Create the application.
app = Flask(__name__)
# API(app) instance to indicate that this is a REST API.
api = Api(app)

# Give SQLite information to SQLAlchemy and link the db instance.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
db = SQLAlchemy(app)

# Base URL for the endpoints.
default_url = 'http://127.0.0.1:5000/'


class TrackModel(db.Model):
    """

    """
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    track = db.Column('track', db.String, nullable=False)
    artist = db.Column('artist', db.String, nullable=False)
    danceability = db.Column('danceability', db.Float, nullable=False)
    key = db.Column('key', db.Integer, nullable=False)
    instrumentalness = db.Column('instrumentalness', db.Float, nullable=False)
    tempo = db.Column('tempo', db.Float, nullable=False)
    duration_ms = db.Column('duration_ms', db.Float, nullable=False)
    popularity = db.Column('popularity', db.Integer, nullable=False)
    decade = db.Column('decade', db.String, nullable=False)

# Fields to use for serialization.
track_fields = {
    'id': fields.Integer,
    'track': fields.String,
    'artist': fields.String,
    'danceability': fields.Float,
    'key': fields.Integer,
    'instrumentalness': fields.Float,
    'tempo': fields.Float,
    'duration_ms': fields.Float,
    'popularity': fields.Integer,
    'decade': fields.String
}

# Parse though the request to check if it meets the defined guidelines.
track_put_args = reqparse.RequestParser()
track_put_args.add_argument('track', type=str, help='Name of the track is required.', required=True)
track_put_args.add_argument('artist', type=str, help='Name of the artist is required.', required=True)
track_put_args.add_argument('danceability', type=float, help='Danceability is required.', required=True)
track_put_args.add_argument('key', type=int, help='Key is required.', required=True)
track_put_args.add_argument('instrumentalness', type=float, help='Instrumentalness is required.', required=True)
track_put_args.add_argument('tempo', type=float, help='Tempo is required.', required=True)
track_put_args.add_argument('duration_ms', type=float, help='Duration is required.', required=True)
track_put_args.add_argument('popularity', type=int, help='Popularity is required.', required=True)
track_put_args.add_argument('decade', type=str, help='Decade is required.', required=True)

# Create Track data access object for communicating with the database.
track_dao = TrackDAO(db, TrackModel)


class TrackList(Resource):

    @marshal_with(track_fields)
    def get_trackmodel(self, track):
        return track

    def get(self):
        page = request.args.get('page', 1, type=int)

        sort_field = request.args.get('sort_field', type=str, default='id')
        sort_order = request.args.get('sort_order', type=str, default='asc')

        filter_field = request.args.get('filter_field', type=str)
        filter_value = request.args.get('filter_value', type=str)

        result = track_dao.get_tracks_list(filter_field, filter_value, sort_field, sort_order, page)

        return result, 200


class Track(Resource):

    @marshal_with(track_fields)
    def put(self, track_id):
        args = track_put_args.parse_args()
        result = track_dao.create_track(args)
        return result, 201

    @marshal_with(track_fields)  # serializes objects of the method
    def get(self, track_id):
        result = track_dao.get_track_by_id(track_id)
        return result, 200

    @marshal_with(track_fields)
    def patch(self, track_id):
        args = track_put_args.parse_args()
        result = track_dao.update_track_by_id(track_id, args)
        return result, 200

    def delete(self, track_id):
        track_dao.delete_track_by_id(track_id)
        return {}, 200


# Define the type of parameters to pass
api.add_resource(Track, '/track/<int:track_id>')
api.add_resource(TrackList, '/tracks/')


@app.route('/')
def index():
    song = Markup("<b>I'm a bolded song!<b>")
    return render_template('index.html', song=song)


@app.route('/alltracks/')
def alltracks():
    page = request.args.get('page')
    if page is None:
        page = 1
    r = requests.get(default_url + '/tracks/' + '?page=' + str(page))
    response = r.json()
    # Response["items"] is jsonified in the api call and jsonified here again, maybe this is bad
    response["items"] = json.loads(response["items"])
    return render_template('tracks.html', pagination=response)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Exception handling
@app.errorhandler(Exception)
def handle_exception(e):
    return {'msg': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)