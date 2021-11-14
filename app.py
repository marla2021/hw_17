# app.py
from create_data import MovieSchema, Movie, DirectorSchema,Director
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movie')
genre_ns =api.namespace('genre')
director_ns =api.namespace('director')


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
    def delete(self,id):
        mov = Movie.query.get(id)
        if mov:
            db.session.delete(mov)
            db.session.commit()
        return '', 204


@movies_ns.route('/?director_id=<int:dir_id>')
class Movie_by_dirView(Resource):
    def get(self, dir_id):
        dir = request.args.get(dir_id)
        direct = Movie.query.filter_by(director_id=dir).all()
        return MovieSchema().dump(direct), 200


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



if __name__ == '__main__':
    app.run(debug=True, port = 8000)
