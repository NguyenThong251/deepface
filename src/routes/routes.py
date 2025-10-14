from flask import request
from src.controls.analyze import AnalyzeController
from src.controls.verify import VerifyController
from src.controls.register import RegisterController


def register_routes(app):

    analyze_controller = AnalyzeController()
    verify_controller = VerifyController()
    register_controller=RegisterController()
    
    def body():
        return request.get_json(force=True, silent=True) or {}

    @app.route("/analyze", methods=["POST"])
    def analyze():
        return analyze_controller.analyze_image(body())

    @app.route("/register", methods=["POST"])
    def register():
        return register_controller.register_user(body())

    @app.route("/verify", methods=["POST"])
    def verify():
        return verify_controller.verify_user(body())

    @app.route("/find", methods=["POST"])
    def find():
        return {"message": "Find endpoint - to be implemented"}, 501