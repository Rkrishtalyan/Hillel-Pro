# ---- Import Statements ----
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# ---- Initialize Extensions ----
db = SQLAlchemy()
"""
Initialize SQLAlchemy for database interactions.

:var db: SQLAlchemy instance used for ORM and database operations.
:type db: flask_sqlalchemy.SQLAlchemy
"""

migrate = Migrate()
"""
Initialize Flask-Migrate for database migrations.

:var migrate: Migrate instance used for managing database schema migrations.
:type migrate: flask_migrate.Migrate
"""
