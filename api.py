# import base64
# import io
# from typing import Any, Dict

# import numpy as np
# from PIL import Image
# from flask import Flask, jsonify, request
# from flask_cors import CORS


# from models.face_detection.Yolo import YoloDetectorClientV12n
# from models.spoofing.FasNet import Fasnet



# app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

# def decode_base64_image(b64_str: str) -> np.ndarray:
#     if "," in b64_str:
#         b64_str = b64_str.split(",", 1)[1]
#     binary = base64.b64decode(b64_str)
#     img = Image.open(io.BytesIO(binary)).convert("RGB")
#     return np.array(img)[:, :, ::-1]


# class Services:
#     def __init__(self):
#         self.detector = YoloDetectorClientV12n()
#         self.spoof = Fasnet()


# services = Services()


# @app.route("/analyze", methods=["POST"])  # detect face -> anti-spoof
# def analyze() -> Any:
#     try:
#         data: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
#         b64 = data.get("image")
#         if not b64:
#             return jsonify({"error": "image (base64) is required"}), 400

#         img = decode_base64_image(b64)

#         faces = services.detector.detect_faces(img)
#         if not faces:
#             return jsonify({"faces": [], "message": "no face"}), 200

#         results = []
#         for face in faces:
#             x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)
#             is_real, score = services.spoof.analyze(img, (x, y, w, h))
#             results.append(
#                 {
#                     "box": {"x": x, "y": y, "w": w, "h": h},
#                     "det_conf": float(face.confidence),
#                     "is_real": bool(is_real),
#                     "spoof_score": float(score),
#                 }
#             )

#         return jsonify({"faces": results}), 200
#     except Exception as err:
#         return jsonify({"error": str(err)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)




import os, base64, io
from typing import Any, Dict
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS

from models.face_detection.Yolo import YoloDetectorClientV12n
from models.spoofing.FasNet import Fasnet

SPOOF_THRESH = float(os.getenv("SPOOF_THRESH", "0.5"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

def decode_base64_image(b64: str) -> np.ndarray:
    if "," in b64: b64 = b64.split(",", 1)[1]
    return np.array(Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB"))[:, :, ::-1]

class Services:
    def __init__(self):
        self.detector = YoloDetectorClientV12n()
        self.spoof = Fasnet()

services = Services()

@app.route("/analyze", methods=["POST"])
def analyze() -> Any:
    try:
        data: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
        b64 = data.get("image")
        if not b64: return jsonify({"error": "image (base64) is required"}), 400

        img = decode_base64_image(b64)
        h, w = img.shape[:2]
        img_is_real, img_score = services.spoof.analyze(img, (0, 0, w, h))
        if img_score >= SPOOF_THRESH and not img_is_real:
            return jsonify({"image_level":{"is_real":bool(img_is_real),"spoof_score":float(img_score),"threshold":SPOOF_THRESH,"label":"spoof"},"faces":[]}), 200

        faces = services.detector.detect_faces(img)
        if not faces:
            return jsonify({"image_level":{"is_real":bool(img_is_real),"spoof_score":float(img_score),"threshold":SPOOF_THRESH,"label":"live"},"faces":[],"message":"no face"}), 200

        results = []
        for f in faces:
            x, y, ww, hh = int(f.x), int(f.y), int(f.w), int(f.h)
            is_real, score = services.spoof.analyze(img, (x, y, ww, hh))
            results.append({"box":{"x":x,"y":y,"w":ww,"h":hh},"det_conf":float(f.confidence),"is_real":bool(is_real),"spoof_score":float(score)})

        any_spoof = any(r["spoof_score"] >= SPOOF_THRESH and not r["is_real"] for r in results)
        final_label = "spoof" if any_spoof else "live"

        return jsonify({"image_level":{"is_real":not any_spoof,"spoof_score":float(img_score),"threshold":SPOOF_THRESH,"label":final_label},"faces":results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
