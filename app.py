from flask import Flask

from flask_cors import CORS
from src.routes.routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)
    register_routes(app)
    return app

app = create_app()
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)