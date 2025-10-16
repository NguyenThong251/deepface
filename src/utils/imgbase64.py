import base64, io, numpy as np
from PIL import Image

def decode_base64_image(b64) -> np.ndarray:
    return np.array(Image.open(io.BytesIO(base64.b64decode(b64.split(",",1)[-1]))).convert("RGB"))[:, :, ::-1]
