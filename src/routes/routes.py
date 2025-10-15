from flask import request
from src.modules.deepface.analyze import AnalyzeController
from src.modules.deepface.verify import VerifyController
from src.modules.deepface.register import RegisterController
from src.modules.deepface.process import ProcessController

def register_routes(app):
    deepface = {
        "analyze": AnalyzeController().analyze_image,
        "verify":  VerifyController().verify_user,
        "register": RegisterController().register_user,
        "process": ProcessController().process_image,
    }
    ekyc = {
        # "verify": EKYCVerifyController().verify_user,
        # "register": EKYCRegisterController().register_user,
    }

    ops = {"deepface": deepface, "ekyc": ekyc}

    def body():
        return request.get_json(force=True, silent=True) or {}


    @app.route("/face/api", methods=["POST"])
    def face_api():
        data = body()
        op   = data.get("_operation")
        mode = data.get("mode")
        if not op or not mode or mode not in ops[op]:
            return {'success': False,"error": {'message':"VALIDATION FAILED"}}
        try:
            return ops[op][mode](data)
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR'}}
