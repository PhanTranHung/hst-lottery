import argparse
from PIL import Image
from TextOCR import Predictor

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="Đường dẫn đến ảnh muốn nhận dạng")
ap.add_argument("-m", "--model", required=True,
    help="Model muốn nhận dạng")
args = vars(ap.parse_args())

def main():

    predictor = Predictor()

    model = args['model']
    image = Image.open(args['image'])

    label = predictor.predict(model, image)
    print('Decoded label = {}'.format(label))

if __name__ == '__main__':
    main()
