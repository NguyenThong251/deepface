from flask import Blueprint, request
from src.modules.ekyc.verify import VerifyController
from src.modules.ekyc.register import RegisterController
from src.modules.ekyc.process import ProcessController
from src.modules.ekyc.userexist import UserExistController
from src.modules.ekyc.redis_face_info import RedisFaceInfoController
from src.routes.middleware import require_auth

erp_face_bp = Blueprint('erp_face', __name__)

ekyc = {
    "userexist": UserExistController().user_exist,
    "delete": UserExistController().delete_face_info,
    "verify":  VerifyController().verify_user,
    "register": RegisterController().register_user,
    "liveness": ProcessController().process_image,
    "redisFaceInfo": RedisFaceInfoController().redis_face_info,
}



ops = { "eKYC": ekyc}

def body():
    return request.get_json(force=True, silent=True) or {}


@erp_face_bp.route("/face/api", methods=["POST"])
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
