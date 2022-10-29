import json
from flask import Flask, send_from_directory, Markup, render_template, request
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from sqlalchemy import literal_column

from alchemy_encoder import AlchemyEncoder

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
db = SQLAlchemy(app)

default_url = 'http://127.0.0.1:5000/'


class TrackModel(db.Model):
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

class TrackList(Resource):

    @marshal_with(track_fields)
    def get_trackmodel(self, track):
        return track

    def get(self):
        page = request.args.get('page', 1, type=int)

        query = TrackModel.query

        sort_field = request.args.get('sort_filed', type=str, default='id')
        sort_order = request.args.get('sort_order', type=str, default='asc')

        # Sort by the user-provided column.
        if sort_order == 'asc':
            query = query.order_by(getattr(TrackModel, sort_field))
        elif sort_order == 'desc':
            query = query.order_by(getattr(TrackModel, sort_field).desc())

        filter_field = request.args.get('filter_field', type=str)
        filter_value = request.args.get('filter_value', type=str)

        if filter_field is not None and filter_value is not None:
            if filter_field in ['track', 'artist']:
                query = query.filter(literal_column(filter_field).like(filter_value))
            else:
                query = query.filter(getattr(TrackModel, filter_field) == filter_value)

        tracks = query.paginate(page=page, per_page=10)
        
        # Iterate instead of returning dictionary at once.
        pages_nums = []
        for page_num in tracks.iter_pages():
            pages_nums.append(page_num)

        items = json.dumps(tracks.items, cls=AlchemyEncoder)
        package = dict(page = tracks.page, has_next = tracks.has_next, has_prev = tracks.has_prev, 
                    tracks_iter = pages_nums, next_num = tracks.next_num, items = items, prev_num = tracks.prev_num)
        
        return package

class Track(Resource):

    @marshal_with(track_fields)
    def put(self, track_id):
        args = track_put_args.parse_args()
        track = TrackModel(**args)
        # Adding entries permanently to the database.
        db.session.add(track)
        db.session.flush() # db.session.commit closes session, does not allow to return tracks
        return track, 201

    @marshal_with(track_fields) # serializes objects of the method
    def get(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        
        if not track:
            raise Exception('Cannot get track, track_id does not exist.')

        return track

    @marshal_with(track_fields)
    def patch(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        if not track:
            raise Exception('Cannot update track, track_id does not exist.')

        args = track_put_args.parse_args()
        TrackModel.query.filter_by(id=track_id).update(args)

        track = TrackModel.query.filter_by(id=track_id).first()
        return track

    def delete(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        if not track:
            raise Exception(f'Cannot delete track, track_id = {track_id} does not exist.')
        db.session.delete(track)
        db.session.commit()

        return {'msg': f'Track with track_id = {track_id} is deleted.'}, 204


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
    print(e)
    return {'msg': str(e)}, 500


if __name__ ==  '__main__':
    app.run(debug=True)
