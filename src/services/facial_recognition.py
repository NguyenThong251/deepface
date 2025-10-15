import numpy as np
import cv2
from typing import Union
from src.models.facial_recognition.GhostFaceNet import GhostFaceNetClient
from src.config.threshold import thresholds


class FacialRecognitionService:
    def __init__(self):
        self.model = GhostFaceNetClient()
        self.model_name = self.model.model_name
        self.distance_metric = "cosine"
    
    def find_cosine_distance(self, source_representation: Union[np.ndarray, list], test_representation: Union[np.ndarray, list]) -> Union[np.float64, np.ndarray]:
        # Convert inputs to numpy arrays if necessary
        source_representation = np.asarray(source_representation)
        test_representation = np.asarray(test_representation)

        if source_representation.ndim == 1 and test_representation.ndim == 1:
            # single embedding
            dot_product = np.dot(source_representation, test_representation)
            source_norm = np.linalg.norm(source_representation)
            test_norm = np.linalg.norm(test_representation)
            distances = 1 - dot_product / (source_norm * test_norm)
        elif source_representation.ndim == 2 and test_representation.ndim == 2:
            # list of embeddings (batch)
            source_normed = self.l2_normalize(source_representation, axis=1)
            test_normed = self.l2_normalize(test_representation, axis=1)
            cosine_similarities = np.dot(test_normed, source_normed.T)
            distances = 1 - cosine_similarities
        else:
            raise ValueError(
                f"Embeddings must be 1D or 2D, but received "
                f"source shape: {source_representation.shape}, test shape: {test_representation.shape}"
            )
        return distances
    
    def l2_normalize(self, x: Union[np.ndarray, list], axis: Union[int, None] = None, epsilon: float = 1e-10) -> np.ndarray:
        x = np.asarray(x)
        norm = np.linalg.norm(x, axis=axis, keepdims=True)
        return x / (norm + epsilon)
    
    def find_threshold(self, model_name: str, distance_metric: str) -> float:
        if thresholds.get(model_name) is None:
            raise ValueError(f"Model {model_name} is not supported.")
        
        threshold = thresholds.get(model_name, {}).get(distance_metric)
        
        if threshold is None:
            raise ValueError(f"Distance metric {distance_metric} is not available for model {model_name}.")
        
        return threshold
    
    def verify(self, img1_path: Union[str, np.ndarray], img2_path: Union[str, np.ndarray]):
        # Handle numpy arrays directly
        if isinstance(img1_path, np.ndarray):
            img1 = img1_path
        else:
            # If path is provided, load image (for future extension)
            img1 = cv2.imread(img1_path)
            
        if isinstance(img2_path, np.ndarray):
            img2 = img2_path
        else:
            img2 = cv2.imread(img2_path)
        
        # Convert BGR to RGB for model input
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        
        # Resize images to model input shape
        img1_resized = cv2.resize(img1_rgb, self.model.input_shape)
        img2_resized = cv2.resize(img2_rgb, self.model.input_shape)
        
        # Normalize images
        img1_normalized = img1_resized.astype(np.float32) / 255.0
        img2_normalized = img2_resized.astype(np.float32) / 255.0
        
        # Get embeddings using the model's forward method
        embedding1 = self.model.forward(img1_normalized)
        embedding2 = self.model.forward(img2_normalized)
        
        # Convert to numpy arrays
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        
        # Calculate distance using proper cosine distance (1 - cosine_similarity)
        distance = self.find_cosine_distance(embedding1, embedding2)
        
        # Get proper threshold for GhostFaceNet
        threshold = self.find_threshold(self.model_name, self.distance_metric)
        
        # Verify: distance <= threshold means same person
        verified = distance <= threshold
        
        return bool(verified)
