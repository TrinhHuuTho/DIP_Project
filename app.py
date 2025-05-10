import streamlit as st



from views.home import Header, Menu, Body, Footer
from views.face_recognition import FaceRecognitionView
from views.fruit_recognition import FruitRecognitionView
from views.image_processing_ch3 import ImageProcessingView
from views.image_processing_ch4 import ImageProcessingCh4View
from views.image_processing_ch5 import ImageProcessingCh5View
from views.image_processing_ch9 import ImageProcessingCh9View
from views.adjust_volume_by_hand import AdjustVolumeView
from views.finger_count import FingerCountView
from views.hand_gesture_recognition import HandGestureRecognitionView

def main():
    choice = Menu()

    # Điều hướng đến từng view
    if choice == "🏠 Trang chủ":
        Header()
        Body()
        Footer()

    elif choice == "📸 Nhận dạng khuôn mặt":
        FaceRecognitionView()

    elif choice == "📷 Nhận dạng trái cây":
        FruitRecognitionView()

    elif choice == "3️⃣ Chương 3":
        ImageProcessingView()

    elif choice == "4️⃣ Chương 4":
        ImageProcessingCh4View()

    elif choice == "5️⃣ Chương 5":
        ImageProcessingCh5View()

    elif choice == "9️⃣ Chương 9":
        ImageProcessingCh9View()

    elif choice == "📸 Điều chỉnh âm lượng bằng cử chỉ":
        AdjustVolumeView()

    elif choice == "📷 Đếm ngón tay":
        FingerCountView()

    elif choice == "...":
        return None

    elif choice == "📞 Liên hệ":
        Footer()

if __name__ == "__main__":
    main()