# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os

# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
 
# Xây dựng hệ thống tham số đầu vào
# -i file ảnh cần nhận dạng
# -p tham số tiền xử lý ảnh (có thể bỏ qua nếu không cần). Nếu dùng: blur : Làm mờ ảnh để giảm noise, thresh: Phân tách đen trắng
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="Đường dẫn đến ảnh muốn nhận dạng")
ap.add_argument("-p", "--preprocesses", type=str, default="red_channel",
	help="Các bước tiền xử lý ảnh. Bao gồm: red_channel, thresh, blur, gray. Các bước phân tách nhau bằng dấy phẩu")
ap.add_argument("-l", "--language", type=str, default="vie",
	help="Ngôn ngữ, mặc định là vie")
ap.add_argument("-d", "--digits", type=int, default=0,
	help="Chỉ nhận diện số")
args = vars(ap.parse_args())

# Đọc file ảnh và chuyển về ảnh xám
image = cv2.imread(args["image"])


r = 700.0 / image.shape[1]
dim = (700, int(image.shape[0] * r))
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)



preprocesses = [element.strip() for element in str(args["preprocesses"]).split(",")]

# Hiển thị các ảnh gốc
cv2.imshow("Image", image)

# Tiền xử lý ảnh
for p in preprocesses: 
	match p:
		case "red_channel":
			# Tách red channel, các thông tin quan trọng trên vé số thường có màu đỏ
			image = image[:,:,1]

		# Loại bỏ vùng màu không cần thiết bằng cách tách ngưỡng
		case "thresh":
			image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

		# Làm mịn đi những chi tiết nhỏ, tránh để model nhận diện
		case "blur":
			image = cv2.bilateralFilter(image, 15, 75, 75)

		# Chuyển qua kênh màu xám
		case "gray":
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# Hiển thị hình ảnh qua từng bước xử lý.
	cv2.imshow(p, image)

options = ""
# check to see if *digit only* OCR should be performed, and if so,
# update our Tesseract OCR options
if args["digits"] > 0:
	options += "outputbase digits"

# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(image, lang=args["language"], config=options)


# In dòng chữ nhận dạng được
print("Kết quả nhận diện:")
print(text)
 

# Đợi chúng ta gõ phím bất kỳ
cv2.waitKey(0)