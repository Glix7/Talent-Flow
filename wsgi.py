"""
WSGI Entry Point for Production.
"""
import os
from app import create_app

# Force production config if not set
if not os.environ.get('FLASK_CONFIG'):
    os.environ['FLASK_CONFIG'] = 'production'

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    app.run()
