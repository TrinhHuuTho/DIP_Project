# DIP_Project
--- 
## Cấu trúc project

- Các file **.py** hiện tại chỉ là ví dụ mẫu nhằm minh họa cho cấu trúc project, các bạn follow để tránh conflicts không đáng có nha. Thanks!

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
└── requirements.txt     # Các thư viện cần cài (streamlit, pandas, numpy, v.v.)
```
---
## Lưu ý:
- Thiết lập **.gitignore** để tránh commit nhầm nhé
- Thiết lập **.env** để tránh rò rỉ thông tin bảo mật nhé
