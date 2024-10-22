import torch
from PIL import Image
from torchvision import transforms as T
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="Đường dẫn đến ảnh muốn nhận dạng")
    ap.add_argument("-m", "--model", required=True,
        help="Model muốn nhận dạng")
    args = vars(ap.parse_args())

    # Load model and image transforms
    parseq = torch.hub.load('./', args['model'], pretrained=True, source='local').eval()
    # img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)
    img_transform = T.Compose([
                T.Resize((32, 128), T.InterpolationMode.BICUBIC),
                T.ToTensor(),
                T.Normalize(0.5, 0.5)
            ])

    img = Image.open(args["image"]).convert('RGB')
    # Preprocess. Model expects a batch of images with shape: (B, C, H, W)
    img = img_transform(img).unsqueeze(0)

    logits = parseq(img)
    logits.shape  # torch.Size([1, 26, 95]), 94 characters + [EOS] symbol

    # Greedy decoding
    pred = logits.softmax(-1)
    label, _ = parseq.tokenizer.decode(pred)
    print('Decoded label = {}'.format(label[0]))

if __name__ == '__main__':
    main()
