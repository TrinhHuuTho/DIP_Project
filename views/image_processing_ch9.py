import streamlit as st
import cv2
import numpy as np
from controllers.image_processing_ch9 import (
    Erosion, Dilation, OpeningClosing, Boundary, HoleFill,
    MyConnectedComponent, ConnectedComponent, CountRice
)

def ImageProcessingCh9View():
    st.markdown(
        """
        <style>
        .image-processing-container {
            text-align: center;
            background-color: #e6f7ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .image-processing-container h3 {
            color: #007acc;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="image-processing-container">
            <h3>📷 Chương 9: Xử lý ảnh hình thái học và đếm đối tượng</h3>
            <p>Tải lên ảnh và chọn phương pháp xử lý ảnh để xem kết quả.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Danh sách các phương pháp xử lý ảnh
    methods = [
        "Erosion", "Dilation", "OpeningClosing", "Boundary",
        "HoleFill", "MyConnectedComponent", "ConnectedComponent", "CountRice"
    ]

    # Chọn phương pháp xử lý
    selected_method = st.selectbox("Chọn phương pháp xử lý", methods)

    # Tải ảnh lên
    uploaded_file = st.file_uploader("Tải lên ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Đọc ảnh từ file
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            st.error("Không thể đọc file ảnh. Vui lòng thử file khác.")
            return

        # Hiển thị ảnh gốc
        st.markdown("#### Ảnh gốc")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption="Ảnh gốc")

        # Xử lý ảnh theo phương pháp được chọn
        try:
            if selected_method == "Erosion":
                result = Erosion(image)
            elif selected_method == "Dilation":
                result = Dilation(image)
            elif selected_method == "OpeningClosing":
                result = OpeningClosing(image)
            elif selected_method == "Boundary":
                result = Boundary(image)
            elif selected_method == "HoleFill":
                result = HoleFill(image)
            elif selected_method == "MyConnectedComponent":
                result = MyConnectedComponent(image)
            elif selected_method == "ConnectedComponent":
                text, result = ConnectedComponent(image)
                st.write(text)
            elif selected_method == "CountRice":
                text, result = CountRice(image)
                st.write(text)

            # Hiển thị ảnh kết quả
            st.markdown("#### Ảnh kết quả")
            if len(result.shape) == 3:  # Ảnh màu
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(result_rgb, caption=f"Kết quả sau khi áp dụng {selected_method}")
            else:  # Ảnh xám
                st.image(result, caption=f"Kết quả sau khi áp dụng {selected_method}", use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi xử lý ảnh: {str(e)}")