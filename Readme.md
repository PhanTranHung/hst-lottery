# Dự án tra cứu kết quả xổ số

## Cấu trúc thư mục

- `.docker`: Chứa các docker file
- `backend`: Chứa code backend
  - `crawl_lottery`: Worker_lottery hiện tại đang làm dở chức năng crawl kqxs của trang `minhngoc.net.vn`
- `misc`: Chứa các dự án thử nghiệm. Chúng tập trung vào demo 1 tính năng duy nhất
  - `parseq`: Nhận diện mã số dự thưởng từ hình ảnh của vé số sử dụng thư viện `torch`
  - `pytesseract`: Nhận diện 3 thông tin của vé số bao gồm: tên đài, ngày xổ, mã số dự thưởng

## Khởi tạo môi trường cho python

Để thuận lợi hơn trong quá trình chạy các project, môi trường này sẽ được sử dụng chung cho tất cả các project.

```bash
make init_env && source .venv/bin/activate
```

## backend/crawl_lottery

Worker này có nhiệm vụ crawl KQXS từ các trang web khác nhau. Hiện tại đang làm dở chức năng crawl kqxs của trang `minhngoc.net.vn`.

Các chạy.

```bash
# Start Mongodb
make up_db


# Start worker
cd backend/crawl_lottery && pip install -r requirements.txt && python app.py
```

Sau khi đã start backend, gọi api để thự hiện quá trình crawl

Api có dạng `http://localhost:8801/craw?channels={channels}&date={date}`

- channels: các tên đài, phân tách nhau bằng dấu phẩy. Xem tất cả tên đài tại [`valid_channels`](/backend/crawl_lottery/crawler/constants.py)
- date: format `dd-mm-yyyy`

Example

```
http://localhost:8801/craw?channels=mien-bac&date=10-10-2024
```

Xem kết quả tại console

## misc/parseq

Mô hình nhận diện mã số dự thưởng sử dụng thư viện `torch`. Mô hình này có kết quả rất tốt, đã được thử trên nhiều vẽ số khác nhau.

**Lưu ý:** Hình ảnh đầu vào chỉ được bao gồm số. Xem [ví dụ này](/misc/lotteries/num.png)

Cách chạy

```bash

cd misc/parseq

# cài đặt thư viện
pip install -r requirements.txt

# sử dụng
python demo.py -i ../../misc/lotteries/num2.png -m "parseq"
```

Xem kết quả ở console.

## misc/pytesseract

Mô hình nhận diện vé số. Nhận diện 3 thông tin của vé số bao gồm: tên đài, ngày xổ, mã số dự thưởng.
Tuy nhiên độ chính xác của mô hình thấp, không nhận diện được các thông tin này. Sử dụng [`misc/parseq`](#miscparseq) để thay thế.

Dựa vào tài liệu này để cài đặt tesseract trên máy: [`Tesseract Installation`](https://tesseract-ocr.github.io/tessdoc/Installation.html)

Cách chạy

```bash
cd misc/pytesseract

 # cài đặt thư viện
pip install -r requirements.txt

# sử dụng
python main.py -i ../lotteries/image.png -p "red_channel,blur" -l vie
```

Xem kết quả ở console.
