"""
Extensions module to initialize SQLAlchemy and other plugins.
Avoids circular imports.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
