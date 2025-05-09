import streamlit as st
import cv2
import numpy as np
from controllers.image_processing_ch3 import (
    Negative, Logarit, Power, PiecewiseLinear, Histogram,
    HistEqual, HistEqualColor, LocalHist, HistStat,
    MyBoxFilter, BoxFilter, Threshold, MedianFilter,
    Sharpen, Gradient
)

def ImageProcessingView():
    st.markdown("### 📷 Chương 3: Xử lý ảnh")
    st.write("Tải lên ảnh và chọn phương pháp xử lý ảnh để xem kết quả.")

    # Danh sách các phương pháp xử lý ảnh
    methods = [
        "Negative", "Logarit", "Power", "PiecewiseLinear", "Histogram",
        "HistEqual", "HistEqualColor", "LocalHist", "HistStat",
        "MyBoxFilter", "BoxFilter", "Threshold", "MedianFilter",
        "Sharpen", "Gradient"
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
            if selected_method == "Negative":
                result = Negative(image)
            elif selected_method == "Logarit":
                result = Logarit(image)
            elif selected_method == "Power":
                result = Power(image)
            elif selected_method == "PiecewiseLinear":
                result = PiecewiseLinear(image)
            elif selected_method == "Histogram":
                result = Histogram(image)
            elif selected_method == "HistEqual":
                result = HistEqual(image)
            elif selected_method == "HistEqualColor":
                result = HistEqualColor(image)
            elif selected_method == "LocalHist":
                result = LocalHist(image)
            elif selected_method == "HistStat":
                result = HistStat(image)
            elif selected_method == "MyBoxFilter":
                result = MyBoxFilter(image)
            elif selected_method == "BoxFilter":
                result = BoxFilter(image)
            elif selected_method == "Threshold":
                result = Threshold(image)
            elif selected_method == "MedianFilter":
                result = MedianFilter(image)
            elif selected_method == "Sharpen":
                result = Sharpen(image)
            elif selected_method == "Gradient":
                result = Gradient(image)

            # Hiển thị ảnh kết quả
            st.markdown("#### Ảnh kết quả")
            if len(result.shape) == 3:  # Ảnh màu
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(result_rgb, caption=f"Kết quả sau khi áp dụng {selected_method}")
            else:  # Ảnh xám
                st.image(result, caption=f"Kết quả sau khi áp dụng {selected_method}", use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi xử lý ảnh: {str(e)}")