# ---- Import Statements ----
from flask import Blueprint, request, jsonify
from app.models import Film, Director
from app.extensions import db
from flask_jwt_extended import jwt_required


# ---- Define Blueprint ----
main = Blueprint('main', __name__)


# ---- Index Route ----
@main.route('/')
def index():
    """
    Display a welcome message.

    :return: A JSON response with a welcome message.
    :rtype: dict
    """
    return {"message": "Welcome to the Film Library API"}


# ---- Director Routes ----

@main.route('/add-director', methods=['POST'])
@jwt_required()
def add_director():
    """
    Add a new director.

    This route accepts a JSON payload with a 'name' field and creates a new director.

    :return: A JSON response with the new director's details or an error message.
    :rtype: dict
    """
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "name is required"}), 400

    director = Director(name=name)
    db.session.add(director)
    db.session.commit()
    return jsonify({"id": director.id, "name": director.name}), 201


@main.route('/directors-list', methods=['GET'])
def get_directors():
    """
    Retrieve a list of all directors.

    :return: A JSON response containing a list of directors.
    :rtype: list
    """
    directors = Director.query.all()
    result = [{"id": d.id, "name": d.name} for d in directors]
    return jsonify(result), 200


@main.route('/update-director/<int:director_id>', methods=['PUT'])
@jwt_required()
def update_director(director_id):
    """
    Update an existing director's name.

    :param director_id: The ID of the director to update.
    :type director_id: int
    :return: A JSON response indicating success or failure.
    :rtype: dict
    """
    director = Director.query.get_or_404(director_id)
    data = request.get_json()
    name = data.get('name')
    if name:
        director.name = name
    db.session.commit()
    return jsonify({"message": "director updated successfully"}), 200


@main.route('/director-delete/<int:director_id>', methods=['DELETE'])
@jwt_required()
def delete_director(director_id):
    """
    Delete a director and reassign their films to 'unknown'.

    :param director_id: The ID of the director to delete.
    :type director_id: int
    :return: A JSON response indicating success or failure.
    :rtype: dict
    """
    director = Director.query.get(director_id)
    if not director:
        return jsonify({"error": "director not found"}), 404

    unknown = Director.query.filter_by(name="unknown").first()
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


# ---- Film Routes ----

@main.route('/films', methods=['POST'])
@jwt_required()
def add_films():
    """
    Add a new film.

    :return: A JSON response with the new film's details or an error message.
    :rtype: dict
    """
    data = request.get_json()
    title = data.get('title')
    release_year = data.get('release_year')
    rating = data.get('rating')
    director_id = data.get('director_id')

    if not all([title, release_year, rating, director_id]):
        return jsonify({"error": "all fields are required"}), 400

    film = Film(
        title=title,
        release_year=int(release_year),
        director_id=int(director_id),
        rating=float(rating)
    )
    db.session.add(film)
    db.session.commit()
    return jsonify({"id": film.id, "title": film.title}), 201


@main.route('/films-list', methods=['GET'])
def get_films():
    """
    Retrieve a list of all films.

    :return: A JSON response containing a list of films with their details.
    :rtype: list
    """
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
@jwt_required()
def delete_film(film_id):
    """
    Delete a film by its ID.

    :param film_id: The ID of the film to delete.
    :type film_id: int
    :return: A JSON response indicating success or failure.
    :rtype: dict
    """
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404

    try:
        db.session.delete(film)
        db.session.commit()
        return jsonify({"message": "film deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/update-film/<int:film_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_film(film_id):
    """
    Update an existing film's details.

    :param film_id: The ID of the film to update.
    :type film_id: int
    :return: A JSON response with updated film details or an error message.
    :rtype: dict
    """
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "no input data provided"}), 400

    try:
        if 'title' in data:
            film.title = data['title']
        if 'release_year' in data:
            film.release_year = int(data['release_year'])
        if 'rating' in data:
            film.rating = float(data['rating'])
        if 'description' in data:
            film.description = data['description']
        if 'director_id' in data:
            director = Director.query.get(data['director_id'])
            if not director:
                return jsonify({"error": "director not found"}), 404
            film.director_id = data['director_id']

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
