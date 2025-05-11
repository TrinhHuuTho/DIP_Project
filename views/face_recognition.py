import streamlit as st
import cv2 as cv
import numpy as np
import joblib
import argparse
import time
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration # type: ignore

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class FaceRecognitionProcessor(VideoProcessorBase):
    def __init__(self, detector, recognizer, svc, mydict):
        self.detector = detector
        self.recognizer = recognizer
        self.svc = svc
        self.mydict = mydict
        # Import visualize and str2bool here to avoid circular import
        from controllers.predict_face import visualize, str2bool
        self.visualize = visualize
        self.str2bool = str2bool

    def preprocess_frame(self, frame):
        # Minimal preprocessing: only adjust brightness and contrast lightly if needed
        alpha = 1.1  # Slightly increase contrast
        beta = 10    # Slightly increase brightness
        frame_eq = cv.convertScaleAbs(frame, alpha=alpha, beta=beta)
        return frame_eq

    def recv(self, frame):
        try:
            # Start timing for performance debugging
            start_time = time.time()

            # Convert frame to OpenCV format
            img_rgb = frame.to_ndarray(format="bgr24")
            print(f"Frame size: {img_rgb.shape}")

            # Convert RGB to BGR for OpenCV processing
            img = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)

            # Preprocess frame with minimal adjustments
            img = self.preprocess_frame(img)

            # Set input size for detector
            self.detector.setInputSize((img.shape[1], img.shape[0]))

            # Detect faces
            faces = self.detector.detect(img)
            num_faces = len(faces[1]) if faces[1] is not None else 0
            print(f"Number of faces detected: {num_faces}")

            # Recognize faces
            predictions = []
            probabilities = []
            if faces[1] is not None:
                for face in faces[1]:
                    face_align = self.recognizer.alignCrop(img, face)
                    face_feature = self.recognizer.feature(face_align)
                    test_predict = self.svc.predict(face_feature)
                    test_proba = self.svc.predict_proba(face_feature)
                    predicted_name = self.mydict[test_predict[0]]
                    max_proba = np.max(test_proba) * 100
                    print(f"Predicted: {predicted_name}, Probability: {max_proba:.2f}%")
                    predictions.append(test_predict[0])
                    probabilities.append(np.max(test_proba))

            # Visualize results (img is in BGR format)
            self.visualize(img, faces, fps=30, predictions=predictions, probabilities=probabilities)

            # Convert BGR back to RGB for WebRTC
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"Frame processing time: {processing_time:.3f} seconds")

            # Return frame in RGB format
            return frame.from_ndarray(img_rgb, format="bgr24")
        except Exception as e:
            print(f"Error in recv: {str(e)}")
            return frame

def FaceRecognitionView():
    st.markdown(
        """
        <style>
        .face-recognition-container {
            text-align: center;
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .face-recognition-container h3 {
            color: #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="face-recognition-container">
            <h3>📸 Nhận dạng khuôn mặt</h3>
            <p>Chọn chế độ để nhận diện khuôn mặt từ webcam hoặc tải lên ảnh.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Khởi tạo mô hình
    @st.cache_resource
    def load_models():
        parser = argparse.ArgumentParser()
        parser.add_argument('--face_detection_model', '-fd', type=str, default='./models/face_detection_yunet_2023mar.onnx')
        parser.add_argument('--face_recognition_model', '-fr', type=str, default='./models/face_recognition_sface_2021dec.onnx')
        parser.add_argument('--score_threshold', type=float, default=0.6)
        parser.add_argument('--nms_threshold', type=float, default=0.3)
        parser.add_argument('--top_k', type=int, default=5000)
        args = parser.parse_args()

        detector = cv.FaceDetectorYN.create(
            args.face_detection_model,
            "",
            (320, 320),
            args.score_threshold,
            args.nms_threshold,
            args.top_k
        )
        recognizer = cv.FaceRecognizerSF.create(args.face_recognition_model, "")
        svc = joblib.load('./models/svc.pkl')
        mydict = ['DuyHao', 'HuuTho', 'HuuThong', 'PhiHiep', 'TrongNghia', 'TrongThuc', 'TuanKiet']
        return detector, recognizer, svc, mydict

    detector, recognizer, svc, mydict = load_models()

    # Tabs cho Livecam và Upload ảnh
    tab1, tab2 = st.tabs(["📹 Livecam", "📤 Tải ảnh lên"])

    with tab1:
        st.write("Sử dụng webcam để nhận diện khuôn mặt theo thời gian thực.")
        
        # Sử dụng streamlit-webrtc để stream video
        webrtc_ctx = webrtc_streamer(
            key="face-recognition",
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=lambda: FaceRecognitionProcessor(detector, recognizer, svc, mydict),
            media_stream_constraints={"video": {"width": {"ideal": 640}, "height": {"ideal": 480}, "frameRate": {"ideal": 50}}, "audio": False},
        )

        if webrtc_ctx.state.playing:
            st.success("Webcam đang hoạt động. Vui lòng đảm bảo ánh sáng tốt để nhận diện chính xác.")
        else:
            st.warning("Vui lòng bật webcam bằng cách nhấn nút Play.")

    with tab2:
        st.write("Tải lên ảnh để nhận diện khuôn mặt.")
        uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Đọc ảnh từ file
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)

            # Thiết lập kích thước đầu vào
            detector.setInputSize((image.shape[1], image.shape[0]))

            # Nhận diện khuôn mặt
            faces = detector.detect(image)
            predictions = []
            probabilities = []
            if faces[1] is not None:
                for face in faces[1]:
                    face_align = recognizer.alignCrop(image, face)
                    face_feature = recognizer.feature(face_align)
                    test_predict = svc.predict(face_feature)
                    test_proba = svc.predict_proba(face_feature)
                    predictions.append(test_predict[0])
                    probabilities.append(np.max(test_proba))

            # Import visualize here to avoid circular import
            from controllers.predict_face import visualize
            # Vẽ kết quả
            visualize(image, faces, fps=0, predictions=predictions, probabilities=probabilities)

            # Hiển thị ảnh kết quả
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            st.image(image_rgb, caption="Kết quả nhận diện khuôn mặt")