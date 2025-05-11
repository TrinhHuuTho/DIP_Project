import streamlit as st

def Header():
    # Thêm CSS toàn cục
    st.markdown(
        """
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
        }
        .header-container {
            text-align: center;
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header-container h1 {
            font-size: 2.5em;
            margin: 0;
        }
        .header-container p {
            font-size: 1.2em;
            margin: 5px 0;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            font-size: 1em;
            margin: 5px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Nội dung tiêu đề
    st.markdown(
        """
        <div class="header-container">
            <h1>📷 Digital Image Processing Project</h1>
            <p>Chào mừng đến Project cuối kỳ môn Xử lý Ảnh Số DIPR430685 - Học kỳ II - Năm học 2024-2025</p>
            <p>TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT HCM</p>
            <p>KHOA CÔNG NGHỆ THÔNG TIN</p>
        </div>
        <div>
            <h3>Nhóm sinh viên:</h3>
            <ul>
                <li>Trịnh Hửu Thọ - 22110238 - Lớp Xử Lý Ảnh Số chiều thứ 3</li>
                <li>Nguyễn Hữu Thông - 22110239 - Lớp Xử Lý Ảnh Số chiều thứ 5</li>
            </ul>
            <h3>Giảng viên hướng dẫn:</h3>
            <ul>
                <li>Trần Tiến Đức</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

def Menu():
    # Thêm CSS cho sidebar
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            border-right: 2px solid #4CAF50;
            padding: 10px;
        }
        [data-testid="stSidebar"] h1 {
            color: #4CAF50;
            font-size: 1.5em;
            text-align: center;
        }
        [data-testid="stSidebar"] .css-1d391kg {
            font-size: 1.1em;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("📌 Menu")

    # Menu chính
    main_menu = [
        "--- Chọn chức năng ---",  # Lựa chọn rỗng
        "🏠 Trang chủ",
        "📸 Nhận dạng khuôn mặt",
        "📷 Nhận dạng trái cây",
        "3️⃣ Chương 3",
        "4️⃣ Chương 4",
        "9️⃣ Chương 9",
        "📞 Liên hệ"
    ]
    main_choice = st.sidebar.selectbox("🔽 Chọn chức năng", main_menu, key="main_menu", index=1)  # Mặc định chọn lựa chọn rỗng

    # Menu Làm thêm (độc lập, hiển thị bên dưới menu chính)
    st.sidebar.title("➕ Phần Làm thêm")
    extra_menu = [
        "📸 Điều chỉnh âm lượng bằng cử chỉ",
        "📷 Đếm ngón tay",
        "📷 Phân loại rác",
        "5️⃣ Chương 5",
        "📞 Liên hệ"
    ]
    extra_choice = st.sidebar.selectbox("🔽 Chọn chức năng", extra_menu, key="extra_menu")

    return main_choice, extra_choice

def Body():
    st.markdown("### 📌 Giới thiệu dự án Xử lý Ảnh Số")
    st.write(
        "📷 Dự án này tập trung vào các kỹ thuật xử lý ảnh số như nhận diện khuôn mặt, phân loại đối tượng, và xử lý ảnh nâng cao. "
        "Sử dụng các thuật toán học máy và thị giác máy tính, ứng dụng giúp phân tích và xử lý ảnh hiệu quả."
    )

    # Chia layout thành 2 phần
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("./images/DIP.jpg", width=400)
        st.caption("🎯 Never give up!")

    with col2:
        st.subheader("✨ Các tính năng chính:")
        st.write("✅ **Nhận diện khuôn mặt** với mô hình học sâu")
        st.write("✅ **Phân loại đối tượng** như trái cây, đồ vật")
        st.write("✅ **Xử lý ảnh** với các bộ lọc và biến đổi")
        st.write("✅ **Trực quan hóa kết quả** với giao diện thân thiện")

def Footer():
    st.markdown("---")
    st.info("⚠️ Ứng dụng hỗ trợ xử lý ảnh và nhận diện đối tượng.")

    st.markdown("### 📞 Thông tin liên hệ")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("📩 **Email trưởng nhóm:** trinhuutho@gmail.com")
        st.write("📌 **Facebook trưởng nhóm:** [Facebook Page](https://www.facebook.com/tho.trinh.56614)")
    with col2:
        st.image("https://byvn.net/Il7R", width=200)
    st.markdown("---")