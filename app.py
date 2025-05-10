from views.home import Header, Menu, Body, Footer
from views.face_recognition import FaceRecognitionView
from views.fruit_recognition import FruitRecognitionView
from views.image_processing_ch3 import ImageProcessingView
from views.image_processing_ch4 import ImageProcessingCh4View
from views.image_processing_ch5 import ImageProcessingCh5View
from views.image_processing_ch9 import ImageProcessingCh9View
from views.adjust_volume_by_hand import AdjustVolumeView
from views.finger_count import FingerCountView
from views.waste_classification import WasteClassificationView

def main():
    main_choice, extra_choice = Menu()

    # Điều hướng đến từng view
    # Ưu tiên main_choice
    if main_choice == "🏠 Trang chủ":
        Header()
        Body()
        Footer()

    elif main_choice == "📸 Nhận dạng khuôn mặt":
        FaceRecognitionView()

    elif main_choice == "📷 Nhận dạng trái cây":
        FruitRecognitionView()

    elif main_choice == "3️⃣ Chương 3":
        ImageProcessingView()

    elif main_choice == "4️⃣ Chương 4":
        ImageProcessingCh4View()

    # elif main_choice == "5️⃣ Chương 5":
    #     ImageProcessingCh5View()

    elif main_choice == "9️⃣ Chương 9":
        ImageProcessingCh9View()

    # Nếu main_choice là "Liên hệ" hoặc không được chọn, kiểm tra extra_choice
    if main_choice == "📞 Liên hệ" or main_choice == "🏠 Trang chủ":
        if extra_choice == "📸 Điều chỉnh âm lượng bằng cử chỉ":
            AdjustVolumeView()

        elif extra_choice == "📷 Đếm ngón tay":
            FingerCountView()

        elif extra_choice == "📷 Phân loại rác":
            WasteClassificationView()

        elif extra_choice == "5️⃣ Chương 5":
            ImageProcessingCh5View()

        elif extra_choice == "📞 Liên hệ":
            Footer()

if __name__ == "__main__":
    main()