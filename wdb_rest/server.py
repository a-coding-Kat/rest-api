from flask import Flask
from flask_restful import Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class TrackModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Float, nullable=False)
    duration_ms = db.Column(db.Float, nullable=False)
    time_signature = db.Column(db.Integer, nullable=False)
    chorus_hit = db.Column(db.Float, nullable=False)
    sections = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)
    decade = db.Column(db.String, nullable=False)


# Fields to use for serialization.
track_fields = {
    'id': fields.Integer,
    'track': fields.String,
    'artist': fields.String,
    'uri': fields.String,
    'danceability': fields.Float,
    'energy': fields.Float,
    'key': fields.Integer,
    'loudness': fields.Float,
    'mode': fields.Integer,
    'speechiness': fields.Float,
    'acousticness': fields.Float,
    'instrumentalness': fields.Float,
    'liveness': fields.Float,
    'valence': fields.Float,
    'tempo': fields.Float,
    'duration_ms': fields.Float,
    'time_signature': fields.Integer,
    'chorus_hit': fields.Float,
    'sections': fields.Integer,
    'popularity': fields.Integer,
    'decade': fields.String
}

class Track(Resource):
    @marshal_with(track_fields) # serializes objects of the method
    def get(self, track_id):
        return {}

    @marshal_with(track_fields)
    def put(self, track_id):
        return {}


# Define the type of parameters to pass
api.add_resource(Track, '/track/<int:track_id>')

if __name__ ==  '__main__':
    app.run(debug=True)
