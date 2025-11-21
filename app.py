from flask import Flask

from flask_cors import CORS
from src.routes.routes import erp_face_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.register_blueprint(erp_face_bp, url_prefix='/erp-api-ekyc/api')
    return app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=False, threaded=True)