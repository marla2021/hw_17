# app.py
from create_data import MovieSchema, Movie, DirectorSchema, Director, Genre
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
genre_ns =api.namespace('genres')
director_ns =api.namespace('directors')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        return MovieSchema(many=True).dump(Movie.query.all()), 200


@movies_ns.route('/<int:id>')
class One_movieView(Resource):
    def get(self, id):
        mov = Movie.query.get(id)
        if not mov:
            movies_ns.abort(404)
        return MovieSchema().dump(mov), 200

    def delete(self,id:int):
        mov = Movie.query.get(id)
        if mov:
            db.session.delete(mov)
            db.session.commit()
        return '', 204


@movies_ns.route('/')
class Movie_by_dirView(Resource):
    def get(self):
        dir_id = request.args.get("director_id")
        gen_id = request.args.get("genre_id")
        if dir_id is not None:
            mov = Movie.query.filter(Movie.director_id == dir_id)
        if gen_id is not None:
            mov = Movie.query.filter(Movie.genre_id == gen_id)
        movies = mov.all()
        return MovieSchema().dump(movies), 200


@director_ns.route('/<int:id>')
class DirView(Resource):
    def delete(self,id:int):
        dir = Director.query.get(id)
        if dir:
            db.session.delete(dir)
            db.session.commit()
        return '', 204

    def put(self, id:int):
        director = Director.query.get(id)
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

@director_ns.route('/')
class Dir2View(Resource):
    def post(self):
        req_json = request.json
        new_dir = Director(**req_json)
        with db.session.begin():
            db.session.add(new_dir)
        return DirectorSchema().dump(new_dir), 201

@genre_ns.route('/<int:id>')
class GenreView(Resource):
    def delete(self,id:int):
        genre = Genre.query.get(id)
        if dir:
            db.session.delete(genre)
            db.session.commit()
        return '', 204

    def put(self, id:int):
        genre = Genre.query.get(id)
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

@genre_ns.route('/')
class New_genreView(Resource):
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return DirectorSchema().dump(new_genre), 201

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
