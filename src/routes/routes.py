from flask import request
from src.controllers.analyze import AnalyzeController
from src.controllers.verify import VerifyController
from src.controllers.register import RegisterController
from src.controllers.process import ProcessController

def register_routes(app):

    analyze_controller = AnalyzeController()
    verify_controller = VerifyController()
    register_controller=RegisterController()
    process_controller=ProcessController()

    def body():
        return request.get_json(force=True, silent=True) or {}

    @app.route("/analyze", methods=["POST"])
    def analyze():
        return analyze_controller.analyze_image(body())

    @app.route("/process", methods=["POST"])
    def process():
        return process_controller.process_image(body())

    @app.route("/register", methods=["POST"])
    def register():
        return register_controller.register_user(body())

    @app.route("/verify", methods=["POST"])
    def verify():
        return verify_controller.verify_user(body())

    @app.route("/find", methods=["POST"])
    def find():
        return {"message": "Find endpoint - to be implemented"}, 501