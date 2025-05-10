import cv2
import mediapipe as mp
import time
import streamlit as st
# pip install python-time
# pip install opencv-python
# pip install mediapipe

def FingerCountView():
    # Page title
    st.markdown("# Đếm Ngón Tay")
    st.markdown("### Hướng dẫn: Sử dụng bàn tay để hiển thị số ngón tay đang giơ lên")
    
    # Khởi tạo các biến cần thiết
    mp_draw = mp.solutions.drawing_utils
    mp_hand = mp.solutions.hands
    tipIds = [4, 8, 12, 16, 20]
    
    # Khởi tạo các biến trạng thái trong session_state
    if 'finger_count_stop' not in st.session_state:
        st.session_state.finger_count_stop = True  # Ban đầu camera tắt
    
    if 'finger_count_started' not in st.session_state:
        st.session_state.finger_count_started = False
    
    # Tạo layout cho các nút điều khiển
    col1, col2 = st.columns(2)
    
    # Nút bật/tắt camera
    with col1:
        if st.session_state.finger_count_stop:
            if st.button("Bật Camera", key="finger_count_start_btn", type="primary"):
                st.session_state.finger_count_stop = False
                st.session_state.finger_count_started = True
                st.rerun()
        else:
            if st.button("Dừng Camera", key="finger_count_stop_btn", type="secondary"):
                st.session_state.finger_count_stop = True
                st.rerun()
    
    # Khởi tạo khung hình ảnh
    FRAME_WINDOW = st.image([])
    
    # Nếu camera chưa được bật, hiển thị hướng dẫn
    if not st.session_state.finger_count_started:
        st.info("Nhấn nút 'Bật Camera' để bắt đầu sử dụng tính năng đếm ngón tay.")
        return
    
    # Nếu camera đã bị dừng, không tiếp tục xử lý
    if st.session_state.finger_count_stop:
        return
    
    # Hiển thị thông báo đang kết nối
    camera_placeholder = st.empty()
    camera_placeholder.info("Đang kết nối với camera...")
    
    # Mở camera
    try:
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Kiểm tra xem camera có mở thành công không
        if not video.isOpened():
            st.error("Không thể kết nối với camera. Vui lòng kiểm tra lại thiết bị camera của bạn.")
            st.session_state.finger_count_stop = True
            st.session_state.finger_count_started = False
            return
        
        # Xóa thông báo đang kết nối
        camera_placeholder.empty()
    except Exception as e:
        st.error(f"Lỗi khi mở camera: {str(e)}")
        st.session_state.finger_count_stop = True
        st.session_state.finger_count_started = False
        return
    
    with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while not st.session_state.finger_count_stop:
            # Capture frame-by-frame
            ret, image = video.read()
            
            # If frame is read correctly ret is True
            if not ret:
                st.error("Không thể đọc frame từ camera. Đang thử lại...")
                continue
            
            # Process the image
            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            except Exception as e:
                st.error(f"Lỗi xử lý hình ảnh: {str(e)}")
                continue
            lmList = []
            if results.multi_hand_landmarks:
                for hand_landmark in results.multi_hand_landmarks:
                    myHands = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHands.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
            fingers = []
            if len(lmList) != 0:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                total = fingers.count(1)

                if total == 0:
                    cv2.putText(image, "No Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

                elif total == 1:
                    cv2.putText(image, "1 Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

                elif total == 2:
                    cv2.putText(image, "2 Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

                elif total == 3:
                    cv2.putText(image, "3 Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

                elif total == 4:
                    cv2.putText(image, "4 Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

                elif total == 5:
                    cv2.putText(image, "5 Finger", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

            # Update the Streamlit UI with the processed frame
            FRAME_WINDOW.image(image, channels='BGR')
            
            # Check if we should stop (controlled by the button outside the loop)
            if st.session_state.finger_count_stop:
                break
                
    # Release the video capture object and clean up
    video.release()
    cv2.destroyAllWindows()
    
    # Show a message when camera is stopped
    if not st.session_state.finger_count_stop:
        st.session_state.finger_count_stop = True
        st.success("Camera đã dừng hoạt động.")
        
    # Thêm nút để bật lại camera
    if st.button("Bật lại camera", key="finger_count_restart_btn"):
        st.session_state.finger_count_stop = False
        st.session_state.finger_count_started = True
        st.rerun()