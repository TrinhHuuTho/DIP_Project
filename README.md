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
│   ├── __init__.py
│   ├── data_model.py     # Ví dụ: load data, xử lý tính toán
│   └── user_model.py     # Ví dụ: thông tin người dùng
│
├── views/               # Thư mục cho tầng View (hiển thị giao diện Streamlit)
│   ├── __init__.py
│   ├── home_view.py      # View trang chủ
│   ├── dashboard_view.py # View dashboard
│   └── form_view.py      # View các form nhập liệu
│
├── controllers/         # Thư mục cho tầng Controller (điều phối logic giữa Model và View)
│   ├── __init__.py
│   ├── home_controller.py
│   ├── dashboard_controller.py
│   └── form_controller.py
│
├── utils/               # Thư viện phụ trợ (helper functions, configs, constants)
│   ├── __init__.py
│   ├── config.py         # Các biến cấu hình chung
│   └── helpers.py        # Các hàm tiện ích
│
├── images/              # Thư mục chứa hình ảnh mẫu hoặc đầu vào
│   ├── ImageProcessing_Chapter3/
│   ├── ImageProcessing_Chapter4/
│   ├── ImageProcessing_Chapter5/
│   └── ImageProcessing_Chapter9/
│
├── models/              # Thư mục chứa các mô hình AI/ML
│   ├── face_detection_yunet_2023mar.onnx
│   ├── face_recognition_sface_2021dec.onnx
│   └── svc.pkl
│
├── requirements.txt     # Các thư viện cần cài (streamlit, pandas, numpy, v.v.)
├── LICENSE              # Thông tin bản quyền
└── README.md            # Tài liệu hướng dẫn dự án
```

## Hướng dẫn cài đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
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

## Bản quyền
Dự án được cấp phép theo [MIT License](LICENSE).
