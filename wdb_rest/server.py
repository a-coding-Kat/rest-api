from flask import Flask, jsonify
from flask_restful import Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
db = SQLAlchemy(app)


class TrackModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    track = db.Column('track', db.String, nullable=False)
    artist = db.Column('artist', db.String, nullable=False)
    uri = db.Column('uri', db.String, nullable=False)
    danceability = db.Column('danceability', db.Float, nullable=False)
    energy = db.Column('energy', db.Float, nullable=False)
    key = db.Column('key', db.Integer, nullable=False)
    loudness = db.Column('loudness', db.Float, nullable=False)
    mode = db.Column('mode', db.Integer, nullable=False)
    speechiness = db.Column('speechiness', db.Float, nullable=False)
    acousticness = db.Column('acousticness', db.Float, nullable=False)
    instrumentalness = db.Column('instrumentalness', db.Float, nullable=False)
    liveness = db.Column('liveness', db.Float, nullable=False)
    valence = db.Column('valence', db.Float, nullable=False)
    tempo = db.Column('tempo', db.Float, nullable=False)
    duration_ms = db.Column('duration_ms', db.Float, nullable=False)
    time_signature = db.Column('time_signature', db.Integer, nullable=False)
    chorus_hit = db.Column('chorus_hit', db.Float, nullable=False)
    sections = db.Column('sections', db.Integer, nullable=False)
    popularity = db.Column('popularity', db.Integer, nullable=False)
    decade = db.Column('decade', db.String, nullable=False)


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
        result = TrackModel.query.filter_by(id=track_id).first()
        return result

    @marshal_with(track_fields)
    def put(self, track_id):
        return {}


# Define the type of parameters to pass
api.add_resource(Track, '/track/<int:track_id>')

if __name__ ==  '__main__':
    app.run(debug=True)
