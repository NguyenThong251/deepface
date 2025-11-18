def face_crop(image, faces):
    if isinstance(faces, dict) and faces.get('success') is False:    
        return faces
    face = faces[0]
    x, y, w, h = int(face.x), int(face.y), int(face.w), int(face.h)
    face_crop = image[y:y+h, x:x+w]
    return face_crop