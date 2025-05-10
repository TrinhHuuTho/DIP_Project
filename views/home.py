import streamlit as st

st.set_page_config(
    page_title="Đồ án cuối kỳ DIP",
    page_icon="☕",
)

def Header():
    st.markdown(
        """
        <div style="text-align:center">
            <h1>📷 Digital Image Processing Project</h1>
            <p style="font-size:18px;">Chào mừng đến Project cuối kỳ môn Xử lý Ảnh Số DIPR430685 - Học kỳ II - Năm học 2024-2025</p>
            <p style="font-size:20px;">TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT HCM</p>
            <p style="font-size:20px;">KHOA CÔNG NGHỆ THÔNG TIN</p>
        </div>
        #Nhóm sinh viên:
        <ul>
            <li>Trịnh Hữu Thọ - 22110238 - Lớp Xử Lý Ảnh Số chiều thứ 3</li>
            <li>Nguyễn Hữu Thông - 22110239 - Lớp Xử Lý Ảnh Số chiều thứ 5</li>
        </ul>
        
        """,
        unsafe_allow_html=True
    )
    st.vega_lite_chart({
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A bar chart showing the distribution of image processing metrics.",
        "data": {
            "values": [
                {"category": "Accuracy", "score": 0.90},
                {"category": "Precision", "score": 0.85},
                {"category": "Recall", "score": 0.88},
                {"category": "F1-Score", "score": 0.87}
            ]
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": "category", "type": "nominal", "title": "Metric"},
            "y": {"field": "score", "type": "quantitative", "title": "Score"},
            "color": {"field": "category", "type": "nominal"}
        }
    })

def Menu():
    st.sidebar.title("📌 Menu")

    # Menu chính
    main_menu = [
        "🏠 Trang chủ",
        "📸 Nhận dạng khuôn mặt",
        "📷 Nhận dạng trái cây",
        "3️⃣ Chương 3",
        "4️⃣ Chương 4",
        "9️⃣ Chương 9",
        "📞 Liên hệ"
    ]
    main_choice = st.sidebar.selectbox("🔽 Chọn chức năng", main_menu, key="main_menu")

    # Menu Làm thêm (độc lập, hiển thị bên dưới menu chính)
    st.sidebar.title("➕ Làm thêm")
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