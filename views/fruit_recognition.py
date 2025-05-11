import streamlit as st
import cv2
import numpy as np
from controllers.fruit_recognition import load_model, recognize_fruit
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration # type: ignore

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class FruitRecognitionProcessor(VideoProcessorBase):
    def __init__(self, net):
        self.net = net

    def recv(self, frame):
        # Convert frame to OpenCV format
        img = frame.to_ndarray(format="bgr24")

        # Nhận diện trái cây
        img = recognize_fruit(img, self.net)

        # Trả lại khung hình đã xử lý
        return frame.from_ndarray(img, format="bgr24")

def FruitRecognitionView():
    st.markdown(
        """
        <style>
        .fruit-recognition-container {
            text-align: center;
            background-color: #fff8dc;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .fruit-recognition-container h3 {
            color: #ff4500;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="fruit-recognition-container">
            <h3>📷 Nhận dạng trái cây</h3>
            <p>Chọn chế độ để nhận diện trái cây từ webcam hoặc tải lên ảnh.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load mô hình YOLOv8n
    @st.cache_resource
    def _load_model():
        return load_model()

    net = _load_model()

    # Tabs cho Livecam và Upload ảnh
    tab1, tab2 = st.tabs(["📹 Livecam", "📤 Tải ảnh lên"])

    with tab1:
        st.write("Sử dụng webcam để nhận diện trái cây theo thời gian thực.")
        
        # Sử dụng streamlit-webrtc để stream video
        webrtc_ctx = webrtc_streamer(
            key="fruit-recognition",
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=lambda: FruitRecognitionProcessor(net),
            media_stream_constraints={"video": {"width": {"ideal": 640}, "height": {"ideal": 480}, "frameRate": {"ideal": 20}}, "audio": False},
        )

        if webrtc_ctx.state.playing:
            st.success("Webcam đang hoạt động. Vui lòng đảm bảo ánh sáng tốt để nhận diện chính xác.")
        else:
            st.warning("Vui lòng bật webcam bằng cách nhấn nút Play.")

    with tab2:
        st.write("Tải lên ảnh để nhận diện trái cây.")
        uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Đọc ảnh từ file
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if image is None:
                st.error("Không thể đọc file ảnh. Vui lòng thử file khác.")
                return

            # Nhận diện trái cây
            result = recognize_fruit(image, net)

            # Hiển thị ảnh kết quả
            st.markdown("#### Ảnh kết quả")
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            st.image(result_rgb, caption="Kết quả nhận diện trái cây")