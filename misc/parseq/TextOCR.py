import torch
from PIL import Image
from torchvision import transforms as T


class Predictor:

    models = ['parseq', 'parseq_tiny', 'abinet', 'crnn', 'trba', 'vitstr']

    def __init__(self):
        self._model_cache = {}
        self._preprocess = T.Compose([
            T.Resize((32, 128), T.InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(0.5, 0.5)
        ])

    def _get_model(self, name):
        if name in self._model_cache:
            return self._model_cache[name]
        model = torch.hub.load('./', name, pretrained=True, trust_repo=True, source='local').eval()
        self._model_cache[name] = model
        return model

    def predict(self, model_name: str, image: Image)-> str:
        model = self._get_model(model_name)
        image = self._preprocess(image.convert('RGB')).unsqueeze(0)

        # Greedy decoding
        pred = model(image).softmax(-1)
        label, _ = model.tokenizer.decode(pred)
        
        return label[0]



 

