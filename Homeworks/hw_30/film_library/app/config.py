# ---- Import Statements ----
import os


# ---- Configuration Class ----
class Config:
    """
    Configure application settings.

    This class defines configuration variables for the Flask application, including
    database connection settings, security keys, and other global options.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///film_library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
