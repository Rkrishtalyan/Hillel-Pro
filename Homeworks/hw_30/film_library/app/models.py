# ---- Import Statements ----
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# ---- Models ----
class User(db.Model):
    """
    Represent a user in the application.

    This model handles user authentication and stores essential user information.

    :var id: Unique identifier for the user.
    :type id: int
    :var username: The username of the user, must be unique.
    :type username: str
    :var password_hash: Hashed password for secure storage.
    :type password_hash: str
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """
        Hash and set the user's password.

        :param password: The plaintext password to hash.
        :type password: str
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify the user's password.

        :param password: The plaintext password to check.
        :type password: str
        :return: True if the password matches the hash, otherwise False.
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Provide a string representation of the user.

        :return: A string representing the user instance.
        :rtype: str
        """
        return f'<User {self.username}>'


class Director(db.Model):
    """
    Represent a film director.

    This model stores information about film directors.

    :var id: Unique identifier for the director.
    :type id: int
    :var name: The name of the director, must be unique.
    :type name: str
    """
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        """
        Provide a string representation of the director.

        :return: A string representing the director instance.
        :rtype: str
        """
        return f'<Director {self.name}>'


class Film(db.Model):
    """
    Represent a film in the library.

    This model stores information about films, including their title, release year,
    rating, description, and the director associated with them.

    :var id: Unique identifier for the film.
    :type id: int
    :var title: The title of the film, must be unique.
    :type title: str
    :var release_year: The year the film was released.
    :type release_year: int
    :var rating: The rating of the film (default is 0.0).
    :type rating: float
    :var poster: URL or path to the film's poster, must be unique.
    :type poster: str
    :var description: A short description of the film, must be unique.
    :type description: str
    :var director_id: Foreign key linking the film to a director.
    :type director_id: int
    :var director: Relationship to the `Director` model.
    :type director: Director
    """
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    poster = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)
    director = db.relationship('Director', backref='films', lazy=True)

    def __repr__(self):
        """
        Provide a string representation of the film.

        :return: A string representing the film instance.
        :rtype: str
        """
        return f'<Film {self.title}>'
