import streamlit as st

def Header():
    st.markdown(
        """
        <div style="text-align:center">
            <h1>📷 Digital Image Processing Project</h1>
            <p style="font-size:18px;">Chào mừng bạn đến với ứng dụng xử lý ảnh số! Đây là dự án môn Xử lý Ảnh Số.</p>
        </div>
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
    # Khởi tạo trạng thái menu trong session_state
    if 'menu_state' not in st.session_state:
        st.session_state.menu_state = "main"

    st.sidebar.title("📌 Menu")

    # Menu chính
    if st.session_state.menu_state == "main":
        menu = [
            "🏠 Trang chủ",
            "📸 Nhận dạng khuôn mặt",
            "📷 Nhận dạng trái cây",
            "3️⃣ Chương 3",
            "4️⃣ Chương 4",
            "5️⃣ Chương 5",
            "9️⃣ Chương 9",
            "➕ Làm thêm",
            "📞 Liên hệ"
        ]
        choice = st.sidebar.selectbox("🔽 Chọn chức năng", menu)

        if choice == "➕ Làm thêm":
            st.session_state.menu_state = "extra"
            st.rerun()  # Sử dụng st.rerun() thay vì st.experimental_rerun()

    # Menu phụ (Làm thêm)
    else:
        menu = [
            "🏠 Trang chủ",
            "📸 Điều chỉnh âm lượng bằng cử chỉ",
            "📷 Đếm ngón tay",
            "...",
            "⬅️ Quay lại",
            "📞 Liên hệ"
        ]
        choice = st.sidebar.selectbox("🔽 Chọn chức năng", menu)

        if choice == "⬅️ Quay lại":
            st.session_state.menu_state = "main"
            st.rerun()  # Sử dụng st.rerun() thay vì st.experimental_rerun()

    return choice

def Body():
    st.markdown("### 📌 Giới thiệu dự án Xử lý Ảnh Số")
    st.write(
        "📷 Dự án này tập trung vào các kỹ thuật xử lý ảnh số như nhận diện khuôn mặt, phân loại đối tượng, và xử lý ảnh nâng cao. "
        "Sử dụng các thuật toán học máy và thị giác máy tính, ứng dụng giúp phân tích và xử lý ảnh hiệu quả."
    )

    # Chia layout thành 2 phần
    col1, col2 = st.columns([1, 1])

    with col1:
        st.video("https://www.youtube.com/watch?v=CMrHM8a3hqw&ab_channel=Simplilearn")
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
        st.write("📩 **Email:** trinhuutho@gmail.com")
        st.write("📌 **Facebook:** [Facebook Page](https://www.facebook.com/tho.trinh.56614)")
    with col2:
        st.image("https://byvn.net/Il7R", width=200)
    st.markdown("---")