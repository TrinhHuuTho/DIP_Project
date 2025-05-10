import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from controllers.waste_classification import load_model, process_image, get_waste_types

# Danh sách tên lớp và ảnh mặc định
class_names = ['RacThaiKinh', 'RacThaiGiay', 'BiaCarton', 'RacHuuCo', 'RacDienTu', 'RacKimLoai']
list_images_trash = [
    '',
    'images/Waste_Classification/1. RacThaiKinh.jpg',
    'images/Waste_Classification/2. RacThaiGiay.jpg',
    'images/Waste_Classification/3. BiaCarton.jpg',
    'images/Waste_Classification/4. RacHuuCo.jpg',
    'images/Waste_Classification/5. RacDienTu.jpg',
    'images/Waste_Classification/6. RacKimLoai.jpg'
]

# Load dữ liệu tái chế
waste_types = get_waste_types()

def WasteClassificationView():
    st.markdown("### 🗑️ Phân loại rác")
    st.write("Chọn loại rác để xem ảnh mặc định hoặc tải lên ảnh để phân loại rác.")

    # Load mô hình YOLOv8 ONNX
    @st.cache_resource
    def _load_model():
        return load_model()

    model = _load_model()

    # Tạo menu chọn loại rác
    st.markdown("#### 🔽 Chọn loại rác")
    selected_trash = st.selectbox(
        "Chọn loại rác",
        ["Tất cả"] + [f"{i}. {name} ({name})" for i, name in enumerate(class_names, 1)]
    )

    # Tạo layout
    col1, col2 = st.columns(2)

    # File uploader
    image_file = st.file_uploader("Tải lên ảnh", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        # Xử lý ảnh được upload
        image = Image.open(image_file)
        col1.image(image, caption="Ảnh đã tải lên", use_container_width=True)

        # Chuyển đổi ảnh cho xử lý
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = img_array[:, :, [2, 1, 0]]  # RGB to BGR
        else:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

        with st.spinner('⏳ Đang phân loại...'):
            processed_img, detection_count, detected_classes, boxes, scores, class_ids, indices = process_image(img_array, selected_trash, model)
            processed_img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
            col2.image(processed_img_rgb, caption="📍 Kết quả phân loại", use_container_width=True)
            st.success(f"✅ Đã phát hiện {detection_count} đối tượng.")

            if detection_count > 0:
                st.subheader("📋 Chi tiết phân loại rác")
                data = []
                for i in indices:
                    box = boxes[i]
                    conf = scores[i]
                    cls_id = class_ids[i]
                    if selected_trash and '(' in selected_trash and ')' in selected_trash:
                        selected_class_name = selected_trash.split('(')[1].strip(')')
                        selected_class_idx = class_names.index(selected_class_name)
                        if cls_id != selected_class_idx:
                            continue
                    cls_name = class_names[cls_id] if cls_id < len(class_names) else f"Class {cls_id}"
                    data.append({
                        "Loại rác": cls_name,
                        "Độ tin cậy": f"{conf:.4f}"
                    })
                st.table(data)

                # Hiển thị hướng dẫn tái chế
                st.subheader("♻️ Hướng dẫn tái chế rác")
                for cls_name in detected_classes:
                    if cls_name in waste_types:
                        st.markdown(f"**{cls_name}**")
                        st.write(f"- **Mô tả**: {waste_types[cls_name]['description']}")
                        st.write(f"- **Hướng dẫn tái chế**: {waste_types[cls_name]['recycling_guidance']}")
                        st.write(f"- **Phương pháp xử lý nếu không tái chế được**: {waste_types[cls_name]['disposal_method']}")
                        st.markdown("---")
                    else:
                        st.warning(f"Không tìm thấy thông tin tái chế cho loại rác: {cls_name}")

    elif selected_trash != "Tất cả":
        # Xử lý ảnh mặc định
        idx = int(selected_trash.split('.')[0])
        default_image_path = list_images_trash[idx]
        if os.path.exists(default_image_path):
            image = Image.open(default_image_path)
            col1.image(image, caption="Ảnh mặc định", use_container_width=True)

            # Chuyển đổi ảnh cho xử lý
            img_array = cv2.imread(default_image_path)
            with st.spinner('⏳ Đang phân loại...'):
                processed_img, detection_count, detected_classes, boxes, scores, class_ids, indices = process_image(img_array, selected_trash, model)
                processed_img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                col2.image(processed_img_rgb, caption="📍 Kết quả phân loại", use_container_width=True)
                st.success(f"✅ Đã phát hiện {detection_count} đối tượng.")

                if detection_count > 0:
                    st.subheader("📋 Chi tiết phân loại rác")
                    data = []
                    for i in indices:
                        box = boxes[i]
                        conf = scores[i]
                        cls_id = class_ids[i]
                        if selected_trash and '(' in selected_trash and ')' in selected_trash:
                            selected_class_name = selected_trash.split('(')[1].strip(')')
                            selected_class_idx = class_names.index(selected_class_name)
                            if cls_id != selected_class_idx:
                                continue
                        cls_name = class_names[cls_id] if cls_id < len(class_names) else f"Class {cls_id}"
                        data.append({
                            "Loại rác": cls_name,
                            "Độ tin cậy": f"{conf:.4f}"
                        })
                    st.table(data)

                    # Hiển thị hướng dẫn tái chế
                    st.subheader("♻️ Hướng dẫn tái chế rác")
                    for cls_name in detected_classes:
                        if cls_name in waste_types:
                            st.markdown(f"**{cls_name}**")
                            st.write(f"- **Mô tả**: {waste_types[cls_name]['description']}")
                            st.write(f"- **Hướng dẫn tái chế**: {waste_types[cls_name]['recycling_guidance']}")
                            st.write(f"- **Phương pháp xử lý nếu không tái chế được**: {waste_types[cls_name]['disposal_method']}")
                            st.markdown("---")
                        else:
                            st.warning(f"Không tìm thấy thông tin tái chế cho loại rác: {cls_name}")
        else:
            st.error(f"Không tìm thấy file ảnh: {default_image_path}")