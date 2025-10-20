thresholds = {
    # "ArcFace": {"cosine": 0.58,"euclidean_l2": 1.077,  "angular": 1.137, "euclidean": 5.14}, #default threshold
    "ArcFace": {"cosine": 0.15,"euclidean_l2": 1.077,  "angular": 1.137, "euclidean": 5.14}, #0.15 cosine 0.25
    # "ArcFace": {"cosine": 0.29,"euclidean_l2": 1.077,  "angular": 1.137, "euclidean": 5.14},
    "VGG-Face": {"cosine": 0.68, "euclidean": 1.17, "euclidean_l2": 1.17, "angular": 0.39},
    "GhostFaceNet": {"cosine": 0.65, "euclidean": 35.71, "euclidean_l2": 1.10, "angular": 0.38},
}
