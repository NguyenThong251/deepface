from flask import request
from src.modules.deepface.verify import VerifyController
from src.modules.deepface.register import RegisterController
from src.modules.deepface.process import ProcessController
from src.modules.deepface.userexist import UserExistController
from src.modules.deepface.redis_face_info import RedisFaceInfoController
from src.routes.middleware import require_auth
def register_routes(app):
    deepface = {
        "userexist": UserExistController().user_exist,
        "delete": UserExistController().delete_face_info,
        "verify":  VerifyController().verify_user,
        "register": RegisterController().register_user,
        "liveness": ProcessController().process_image,
        "redisFaceInfo": RedisFaceInfoController().redis_face_info,

    }
    ekyc = {
        # "verify": EKYCVerifyController().verify_user,
        # "register": EKYCRegisterController().register_user,
    }

    ops = {"Deepface": deepface, "ekyc": ekyc}

    def body():
        return request.get_json(force=True, silent=True) or {}


    @app.route("/face/api", methods=["POST"])
    # @require_auth # authentication required
    def face_api():
        data = body()
        op   = data.get("_operation")
        mode = data.get("mode")
        if not op or not mode or mode not in ops[op]:
            return {'success': False,"error": {'code':"VALIDATION_FAILED",
                'message': "Operation not found" if not op else "Mode not found"}}
        try:
            return ops[op][mode](data)
        except Exception as e:
            return {'success': False,"error": {'message': 'SYSTEM ERROR'}}
