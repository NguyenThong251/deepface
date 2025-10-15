from src.models.spoofing.FasNet import Fasnet


class AntiSpoofService:
    def __init__(self,  threshold: float = 0.5):
        self.spoof = Fasnet()
        self.threshold = threshold
    
    def analyze_image(self, img, facial_area):
        return self.spoof.analyze(img, facial_area)
