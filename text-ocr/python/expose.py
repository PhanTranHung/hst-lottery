from PIL import Image
from TextOCR import Predictor

predictor = Predictor()

def predict(model: str, image: Image):
    label = predictor.predict(model, image)
    return label