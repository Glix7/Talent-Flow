from flask import Flask
from config import config
from app.extensions import db

def create_app(config_name='default'):
    """
    Application Factory to create Flask app instance.
    
    Args:
        config_name (str): Configuration environment (default, development, production)
        
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions
    db.init_app(app)

    # Register Blueprints / Routes
    from app.routes import blueprint as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create Database Tables (for demo simplicity)
    with app.app_context():
        db.create_all()

    return app
