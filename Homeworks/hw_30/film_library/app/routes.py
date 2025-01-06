from flask import Blueprint, request, jsonify
from app.models import Film, Director
from app.extensions import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return {"message": "Welcome to the Film Library API"}


@main.route('/add-director', methods=['POST'])
def add_director():
    data = request.get_json()
    name = data['name']
    if not name:
        return jsonify({"error: name is required"}), 400
    director = Director(name=name)
    db.session.add(director)
    db.session.commit()
    return jsonify({"id": director.id, "name": director.name}), 201


@main.route('/directors-list', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    result = [{"id": d.id, "name": d.name} for d in directors]
    return jsonify(result), 200


@main.route('/update-director/<int:director_id>', methods=['PUT'])
def update_director(director_id):
    director = Director.query.get_or_404(director_id)
    data = request.get_json()
    name = data['name']
    if name:
        director.name = name
    db.session.commit()
    return jsonify({"message": "director updated successfully"}), 200


@main.route('/director-delete/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    director = Director.query.get(director_id)
    if not director:
        return jsonify({"error": "director not found"}), 404
    unknown = director.query.filter_by(name="unknown").first()
    if not unknown:
        unknown = Director(name="unknown")
        db.session.add(unknown)
        db.session.commit()
    for film in director.films:
        film.director_id = unknown.id
        db.session.add(film)
    db.session.delete(director)
    db.session.commit()
    return jsonify({"message": "director deleted successfully"}), 200


@main.route('/films', methods=['POST'])
def add_films():
    data = request.get_json()
    title = data.get('title')
    release_year = data.get('release_year')
    rating = data.get('rating')
    director_id = data.get('director_id')
    if not all([title, release_year, rating, director_id]):
        return jsonify({"error": "all fields are required"}), 400
    film = Film(title=title, release_year=int(release_year), director_id=int(director_id), rating=float(rating))
    db.session.add(film)
    db.session.commit()
    return jsonify({"id": film.id, "title": film.title}), 201


@main.route('/films-list', methods=['GET'])
def get_films():
    films = Film.query.all()
    result = [{
        "id": f.id,
        "title": f.title,
        "release_year": f.release_year,
        "rating": f.rating,
        "director": f.director.name,
    } for f in films]
    return jsonify(result), 200


@main.route('/delete-film/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404
    try:
        db.session.delete(film)
        db.session.commit()
        return jsonify({"message": "film deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/update-film/<int:film_id>', methods=['PUT, PATCH'])
def update_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "no input data provided"}), 400
    try:
        if 'title' in data:
            film.title = data['title']
        if "release_year" in data:
            film.release_year = int(data['release_year'])
        if 'rating' in data:
            film.rating = float(data['rating'])
        if 'description' in data:
            film.description = data['description']
        if 'director_id' in data:
            director = Director.query.get(data['director_id'])
            if not director:
                return jsonify({"error": "director not found"}), 404
            film.director_id = data["director_id"]

        db.session.commit()
        return jsonify({"message": "film updated successfully", "film": {
            "id": film.id,
            "title": film.title,
            "release_year": film.release_year,
            "rating": film.rating,
            "description": film.description,
            "director_id": film.director_id
        }}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
