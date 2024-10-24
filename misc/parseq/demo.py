import torch
from PIL import Image
import argparse
from torchvision import transforms as T


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="Đường dẫn đến ảnh muốn nhận dạng, lưu ý: ảnh chỉ được bao gồm số")
ap.add_argument("-m", "--model", required=True,
    help="Model muốn nhận dạng, hiện tại hỗ trợ: `abinet`, `crnn`, `trba`, `vitstr`, `parseq_tiny`, `parseq_patch16_224`, `parseq`")
args = vars(ap.parse_args())



model = torch.hub.load('./', args['model'], pretrained=True, source='local').eval()
preprocess = T.Compose([
            T.Resize((32, 128), T.InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(0.5, 0.5)
        ])

image = Image.open(args["image"]).convert('RGB')
image = preprocess(image).unsqueeze(0)
pred = model(image).softmax(-1)
label, _ = model.tokenizer.decode(pred)
print('Image path = "{}"'.format(args["image"]))
print('Decoded label = {}'.format(label))


