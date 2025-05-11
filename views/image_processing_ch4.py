import streamlit as st
import cv2
import numpy as np
from controllers.image_processing_ch4 import (
    Spectrum, FrequencyFilter, DrawNotchRejectFilter, RemoveMoire
)

def ImageProcessingCh4View():
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
            <h3>📷 Chương 4: Xử lý ảnh trong miền tần số</h3>
            <p>Tải lên ảnh và chọn phương pháp xử lý ảnh để xem kết quả.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Danh sách các phương pháp xử lý ảnh
    methods = [
        "Spectrum", "FrequencyFilter", "DrawNotchRejectFilter", "RemoveMoire"
    ]

    # Chọn phương pháp xử lý
    selected_method = st.selectbox("Chọn phương pháp xử lý", methods)

    # Tải ảnh lên (trừ DrawNotchRejectFilter không cần ảnh đầu vào)
    if selected_method != "DrawNotchRejectFilter":
        uploaded_file = st.file_uploader("Tải lên ảnh", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = None

    if (uploaded_file is not None) or (selected_method == "DrawNotchRejectFilter"):
        # Đọc ảnh từ file (nếu có)
        if uploaded_file is not None:
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
            if selected_method == "Spectrum":
                result = Spectrum(image)
            elif selected_method == "FrequencyFilter":
                result = FrequencyFilter(image)
            elif selected_method == "DrawNotchRejectFilter":
                result = DrawNotchRejectFilter()
            elif selected_method == "RemoveMoire":
                result = RemoveMoire(image)

            # Hiển thị ảnh kết quả
            st.markdown("#### Ảnh kết quả")
            if len(result.shape) == 3:  # Ảnh màu
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(result_rgb, caption=f"Kết quả sau khi áp dụng {selected_method}")
            else:  # Ảnh xám
                st.image(result, caption=f"Kết quả sau khi áp dụng {selected_method}", use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi xử lý ảnh: {str(e)}")