import cv2
import numpy as np

# Ánh xạ tên trái cây từ tiếng Anh sang tiếng Việt
fruit_name_mapping = {
    "apple": "Tao",
    "banana": "Chuoi",
    "guava": "Oi",
    "lemon": "Chanh",
    "orange": "Cam",
    "pomegranate": "Luu",
    "sau_rieng": "Sau rieng",
    "pitaya": "Thanh long"
}

# Danh sách class của mô hình
class_names = ['apple', 'banana', 'guava', 'lemon', 'orange', 'pomegranate', 'sau_rieng', 'pitaya']

def load_model():
    # Load mô hình YOLOv8n ONNX
    net = cv2.dnn.readNetFromONNX("./models/yolov8n_fruit_v2.onnx")
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

    # Đầu ra của YOLOv8 ONNX có dạng (1, 13, 8400)
    # Cần chuyển thành (8400, 13) để mỗi hàng là một box dự đoán
    try:
        # Kiểm tra số chiều của outputs
        if len(outputs.shape) == 3:
            detections = outputs[0]  # Shape: (13, 8400)
            detections = np.transpose(detections, (1, 0))  # Shape: (8400, 13)
        elif len(outputs.shape) == 2:
            detections = outputs  # Shape: (8400, 13)
        else:
            raise ValueError(f"Unexpected output shape: {outputs.shape}")

        boxes = []
        scores = []
        class_ids = []

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

        # Áp dụng Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, iou_threshold)
        if len(indices) > 0:
            indices = indices.flatten()
        else:
            indices = []

    except Exception as e:
        print(f"Error in postprocessing: {str(e)}")
        boxes, scores, class_ids, indices = [], [], [], []

    return boxes, scores, class_ids, indices

def draw_detections(image, boxes, scores, class_ids, indices):
    for i in indices:
        x, y, w, h = boxes[i]
        score = scores[i]
        class_id = class_ids[i]

        # Lấy tên trái cây tiếng Việt
        fruit_name_en = class_names[class_id]
        fruit_name_vn = fruit_name_mapping.get(fruit_name_en, fruit_name_en)

        # Vẽ bounding box và nhãn
        color = (0, 255, 0)  # Màu xanh lá
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        label = f"{fruit_name_vn}: {score:.2f}"
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return image

def recognize_fruit(image, net):
    # Tiền xử lý ảnh
    blob = preprocess_image(image)
    
    # Đặt đầu vào cho mô hình
    net.setInput(blob)
    
    # Chạy mô hình
    outputs = net.forward()
    
    # Xử lý hậu kỳ
    boxes, scores, class_ids, indices = postprocess_output(outputs, image.shape)
    
    # Vẽ kết quả lên ảnh
    result = draw_detections(image, boxes, scores, class_ids, indices)
    return result