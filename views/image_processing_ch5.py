import streamlit as st
import cv2
import numpy as np
from controllers.image_processing_ch5 import (
    CreateMotionNoise, DenoiseMotion, WienerFilter, HistEqual
)

def ImageProcessingCh5View():
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
            <h3>📷 Chương 5: Xử lý ảnh trong miền tần số và khử nhiễu</h3>
            <p style="color: #007acc;">Tải lên ảnh và chọn phương pháp xử lý ảnh để xem kết quả.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Danh sách các phương pháp xử lý ảnh
    methods = [
        "CreateMotionNoise", "DenoiseMotion", "WienerFilter", "HistEqual"
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
            if selected_method == "CreateMotionNoise":
                result = CreateMotionNoise(image)
            elif selected_method == "DenoiseMotion":
                result = DenoiseMotion(image)
            elif selected_method == "WienerFilter":
                kernel_size = st.slider("Kích thước kernel", 3, 15, 3, step=2)
                K = st.slider("Hằng số K", 1, 50, 10)
                result = WienerFilter(image, kernel_size=kernel_size, K=K)
            elif selected_method == "HistEqual":
                result = HistEqual(image)

            # Hiển thị ảnh kết quả
            st.markdown("#### Ảnh kết quả")
            if len(result.shape) == 3:  # Ảnh màu
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(result_rgb, caption=f"Kết quả sau khi áp dụng {selected_method}")
            else:  # Ảnh xám
                st.image(result, caption=f"Kết quả sau khi áp dụng {selected_method}", use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi xử lý ảnh: {str(e)}")