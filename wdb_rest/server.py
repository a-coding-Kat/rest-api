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
    danceability = db.Column('danceability', db.Float, nullable=False)
    loudness = db.Column('loudness', db.Float, nullable=False)
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
    'loudness': fields.Float,
    'instrumentalness': fields.Float,
    'tempo': fields.Float,
    'duration_ms': fields.Float,
    'popularity': fields.Integer,
    'decade': fields.String
}

class Track(Resource):
    @marshal_with(track_fields)
    def put(self, track_id):
        return {}

    @marshal_with(track_fields) # serializes objects of the method
    def get(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        if not track:
            raise Exception('Cannot get track, track_id does not exist.')

        return track

    @marshal_with(track_fields)
    def post(self, track_id):
        return {}

    def delete(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        if not track:
            raise Exception(f'Cannot delete track, track_id = {track_id} does not exist.')
        db.session.delete(track)
        db.session.commit()

        return {'msg': f'Track with track_id = {track_id} is deleted.'}, 204


# Define the type of parameters to pass
api.add_resource(Track, '/track/<int:track_id>')


# Exception handling
@app.errorhandler(Exception)
def handle_exception(e):
    return {'msg': str(e)}, 500


if __name__ ==  '__main__':
    app.run(debug=True)
