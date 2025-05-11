# DIP_Project

## Giới thiệu
DIP_Project là một ứng dụng xử lý ảnh được xây dựng bằng Python, sử dụng Streamlit để hiển thị giao diện người dùng. Dự án được tổ chức theo mô hình MVC (Model-View-Controller) để dễ dàng quản lý và mở rộng.

## Cấu trúc project

```shell
DIP_PROJECT/
│
├── app.py               # Điểm bắt đầu chạy app Streamlit
│
├── models/              # Thư mục cho tầng Model (xử lý dữ liệu, business logic)
│   ├── face_detection_yunet_2023mar.onnx
│   ├── face_recognition_sface_2021dec.onnx
│   ├── svc.pkl
│   ├── waste_classification.onnx
│   ├── waste_classification.pt
│   ├── yolov8n_fruit_v2.onnx
│   ├── yolov8n_fruit_v2.pt
│   ├── yolov8n_fruit.onnx
│   └── yolov8n_fruit.pt
│
├── views/               # Thư mục cho tầng View (hiển thị giao diện Streamlit)
│   ├── adjust_volume_by_hand.py  # Giao diện điều chỉnh âm lượng bằng cử chỉ
│   ├── face_recognition.py       # Giao diện nhận dạng khuôn mặt
│   ├── finger_count.py           # Giao diện đếm ngón tay
│   ├── fruit_recognition.py      # Giao diện nhận dạng trái cây
│   ├── home.py                   # Giao diện trang chủ
│   ├── image_processing_ch3.py   # Giao diện xử lý ảnh chương 3
│   ├── image_processing_ch4.py   # Giao diện xử lý ảnh chương 4
│   ├── image_processing_ch5.py   # Giao diện xử lý ảnh chương 5
│   ├── image_processing_ch9.py   # Giao diện xử lý ảnh chương 9
│   └── waste_classification.py   # Giao diện phân loại rác
│
├── controllers/         # Thư mục cho tầng Controller (điều phối logic giữa Model và View)
│   ├── fruit_recognition.py
│   ├── handDetectionModule.py
│   ├── image_processing_ch3.py
│   ├── image_processing_ch4.py
│   ├── image_processing_ch5.py
│   ├── image_processing_ch9.py
│   ├── predict_face.py
│   └── waste_classification.py
│
├── utils/               # Thư viện phụ trợ (helper functions, configs, constants)
│   ├── __init__.py
│   ├── config.py         # Các biến cấu hình chung
│   └── helpers.py        # Các hàm tiện ích
│
├── images/              # Thư mục chứa hình ảnh mẫu hoặc đầu vào
│   ├── DIP.jpg
│   ├── FaceImg/
│   ├── FingerImages/
│   ├── FruitImg/
│   ├── ImageProcessing_Chapter3/
│   ├── ImageProcessing_Chapter4/
│   ├── ImageProcessing_Chapter5/
│   ├── ImageProcessing_Chapter9/
│   └── Waste_Classification/
│
├── data/                # Thư mục chứa dữ liệu bổ trợ
│   └── waste_guide.json
│
├── requirements.txt     # Danh sách các thư viện cần cài đặt
├── LICENSE              # Thông tin bản quyền
└── README.md            # Tài liệu hướng dẫn dự án
```

## Hướng dẫn cài đặt

1. **Clone repository**:
   ```bash
   git clone https://github.com/TrinhHuuTho/DIP_Project.git
   cd DIP_Project
   ```

2. **Tạo môi trường ảo**:
   ```bash
   python -m venv .myvenv
   source .myvenv/bin/activate  # Trên Linux/MacOS
   .myvenv\Scripts\activate     # Trên Windows
   ```

3. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy ứng dụng**:
   ```bash
   streamlit run app.py
   ```

## Lưu ý
- Thiết lập **.gitignore** để tránh commit nhầm các file không cần thiết.
- Thiết lập **.env** để bảo mật thông tin nhạy cảm như API keys, database credentials, v.v.

## Đóng góp

Chúng tôi hoan nghênh mọi đóng góp để cải thiện dự án này. Nếu bạn muốn đóng góp, vui lòng làm theo các bước sau:

1. **Fork repository**:
   - Nhấn nút "Fork" trên GitHub để tạo một bản sao của repository này trên tài khoản của bạn.

2. **Clone repository**:
   ```bash
   git clone https://github.com/<your-username>/DIP_Project.git
   cd DIP_Project
   ```

3. **Tạo nhánh mới**:
   - Tạo một nhánh mới để làm việc trên tính năng hoặc sửa lỗi của bạn.
   ```bash
   git checkout -b feature/ten-tinh-nang
   ```

4. **Thực hiện thay đổi**:
   - Thực hiện các thay đổi cần thiết và commit chúng.
   ```bash
   git add .
   git commit -m "Mô tả ngắn gọn về thay đổi của bạn"
   ```

5. **Push nhánh của bạn**:
   ```bash
   git push origin feature/ten-tinh-nang
   ```

6. **Tạo Pull Request**:
   - Truy cập repository gốc trên GitHub và tạo một Pull Request từ nhánh của bạn.

7. **Thảo luận và hợp nhất**:
   - Chờ phản hồi từ nhóm phát triển. Nếu cần, bạn có thể được yêu cầu thực hiện thêm các thay đổi trước khi Pull Request được hợp nhất.

Cảm ơn bạn đã đóng góp cho dự án!

## Bản quyền
Dự án được cấp phép theo [MIT License](LICENSE).
