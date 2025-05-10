import cv2
import numpy as np
import json

# Đường dẫn model ONNX
model_path = "./models/waste_classification.onnx"

# Đường dẫn file JSON
json_path = "./data/waste_guide.json"

# Danh sách tên lớp
class_names = ['RacThaiKinh', 'RacThaiGiay', 'BiaCarton', 'RacHuuCo', 'RacDienTu', 'RacKimLoai']

# Danh sách ảnh mặc định
list_images_trash = [
    '',
    'images/Waste_Classification/1. RacThaiKinh.jpg',
    'images/Waste_Classification/2. RacThaiGiay.jpg',
    'images/Waste_Classification/3. BiaCarton.jpg',
    'images/Waste_Classification/4. RacHuuCo.jpg',
    'images/Waste_Classification/5. RacDienTu.jpg',
    'images/Waste_Classification/6. RacKimLoai.jpg'
]

# Đọc dữ liệu từ file JSON
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        waste_types = data.get("waste_types", {})
except FileNotFoundError:
    print(f"Không tìm thấy file {json_path}. Vui lòng kiểm tra đường dẫn.")
    waste_types = {}
except json.JSONDecodeError:
    print(f"File {json_path} không đúng định dạng JSON. Vui lòng kiểm tra nội dung file.")
    waste_types = {}

def load_model():
    # Load mô hình YOLOv8 ONNX với OpenCV DNN
    net = cv2.dnn.readNetFromONNX(model_path)
    return net

def preprocess_image(image, input_size=(640, 640)):
    # Resize ảnh về kích thước đầu vào của YOLOv8
    blob = cv2.dnn.blobFromImage(image, 1/255.0, input_size, swapRB=True, crop=False)
    return blob

def postprocess_output(outputs, image_shape, conf_threshold=0.5, iou_threshold=0.4):
    # Lấy kích thước gốc của ảnh
    orig_h, orig_w = image_shape[:2]
    input_size = 640  # Kích thước đầu vào của YOLOv8
    
    # In shape của outputs để debug
    print(f"Outputs shape: {outputs.shape}")

    # Đầu ra của YOLOv8 ONNX có dạng (1, 10, 8400) với 6 class + 4 tọa độ
    try:
        if len(outputs.shape) == 3:
            detections = outputs[0]  # Shape: (10, 8400)
            detections = np.transpose(detections, (1, 0))  # Shape: (8400, 10)
        elif len(outputs.shape) == 2:
            detections = outputs  # Shape: (8400, 10)
        else:
            raise ValueError(f"Unexpected output shape: {outputs.shape}")

        boxes = []
        scores = []
        class_ids = []
        detected_classes = set()  # Lưu các loại rác được phát hiện

        for detection in detections:
            # Lấy tọa độ và độ tin cậy
            x_center, y_center, width, height = detection[:4]
            confidences = detection[4:]  # Điểm tin cậy cho từng class
            print(f"Number of classes in confidences: {len(confidences)}")  # Debug số class
            confidence = np.max(confidences)  # Lấy điểm tin cậy cao nhất
            class_id = np.argmax(confidences)  # Lấy class có điểm cao nhất

            # Kiểm tra class_id hợp lệ
            if class_id >= len(class_names):
                print(f"Invalid class_id {class_id}, skipping detection")
                continue

            if confidence > conf_threshold:
                # Chuyển đổi tọa độ từ không gian tỷ lệ về không gian gốc
                x_center = x_center * orig_w / input_size
                y_center = y_center * orig_h / input_size
                width = width * orig_w / input_size
                height = height * orig_h / input_size

                x = int(x_center - width / 2)
                y = int(y_center - height / 2)
                w = int(width)
                h = int(height)

                boxes.append([x, y, w, h])
                scores.append(float(confidence))
                class_ids.append(int(class_id))
                detected_classes.add(class_names[class_id])

        # Áp dụng Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, iou_threshold)
        if len(indices) > 0:
            indices = indices.flatten()
        else:
            indices = []

    except Exception as e:
        print(f"Error in postprocessing: {str(e)}")
        boxes, scores, class_ids, indices, detected_classes = [], [], [], [], set()

    return boxes, scores, class_ids, indices, detected_classes

def process_image(img_array, selected_class=None, model=None):
    if model is None:
        raise ValueError("Model không được cung cấp.")

    # Tiền xử lý ảnh
    blob = preprocess_image(img_array)
    
    # Đặt đầu vào cho mô hình
    model.setInput(blob)
    
    # Chạy mô hình
    outputs = model.forward()
    
    # Xử lý hậu kỳ
    boxes, scores, class_ids, indices, detected_classes = postprocess_output(outputs, img_array.shape)
    
    # Vẽ kết quả lên ảnh
    processed_img = draw_detections(img_array, boxes, scores, class_ids, indices)
    detection_count = len(indices)

    return processed_img, detection_count, detected_classes, boxes, scores, class_ids, indices

def draw_detections(image, boxes, scores, class_ids, indices):
    output_img = image.copy()
    
    for i in indices:
        x, y, w, h = boxes[i]
        score = scores[i]
        class_id = class_ids[i]

        cls_name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"

        cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f"{cls_name}: {score:.2f}"
        (label_width, label_height), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(output_img, (x, y - label_height - baseline),
                     (x + label_width, y), (255, 255, 255), cv2.FILLED)
        cv2.putText(output_img, label, (x, y - baseline),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    return output_img

def get_waste_types():
    return waste_types