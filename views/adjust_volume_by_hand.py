import cv2
import numpy as np
import pycaw
import controllers.handDetectionModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import streamlit as st

def AdjustVolumeView():
    # Page title
    st.markdown("# Điều khiển volume bằng cử chỉ")
    st.markdown("### Hướng dẫn: Sử dụng ngón cái và ngón trỏ để điều chỉnh âm lượng")
    
    # Khởi tạo các biến trạng thái trong session_state
    if 'volume_stop' not in st.session_state:
        st.session_state.volume_stop = True  # Ban đầu camera tắt
    
    if 'volume_started' not in st.session_state:
        st.session_state.volume_started = False
    
    # Tạo layout cho các nút điều khiển
    col1, col2 = st.columns(2)
    
    # Nút bật/tắt camera
    with col1:
        if st.session_state.volume_stop:
            if st.button("Bật Camera", key="volume_start_btn", type="primary"):
                st.session_state.volume_stop = False
                st.session_state.volume_started = True
                st.rerun()
        else:
            if st.button("Dừng Camera", key="volume_stop_btn", type="secondary"):
                st.session_state.volume_stop = True
                st.rerun()
    
    # Khởi tạo khung hình ảnh
    FRAME_WINDOW = st.image([])
    
    # Nếu camera chưa được bật, hiển thị hướng dẫn
    if not st.session_state.volume_started:
        st.info("Nhấn nút 'Bật Camera' để bắt đầu sử dụng tính năng điều chỉnh âm lượng.")
        return
    
    # Nếu camera đã bị dừng, không tiếp tục xử lý
    if st.session_state.volume_stop:
        return
        
    # Initialize COM library before accessing audio devices
    try:
        comtypes.CoInitialize()
        
        # access system's volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        volMin = volRange[0]
        volMax = volRange[1]
    except Exception as e:
        st.error(f"Lỗi khi truy cập âm thanh hệ thống: {str(e)}")
        st.session_state.volume_stop = True
        st.session_state.volume_started = False
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
            comtypes.CoUninitialize()
            st.session_state.volume_stop = True
            st.session_state.volume_started = False
            return
        
        # Xóa thông báo đang kết nối
        camera_placeholder.empty()
    except Exception as e:
        st.error(f"Lỗi khi mở camera: {str(e)}")
        comtypes.CoUninitialize()
        st.session_state.volume_stop = True
        st.session_state.volume_started = False
        return
        
    # Khởi tạo đối tượng phát hiện bàn tay
    detect = htm.handDetector()
    
    # setting the captured video's dimensions if needed
    # wCam, hCam = 1920, 1080
    # video.set(3, wCam)
    # video.set(4, hCam)

    detect = htm.handDetector()  # make an object for hand detection module

    while not st.session_state.volume_stop:
        # Capture frame-by-frame
        check, frame = video.read()  # check & capture the frame
        
        # If frame is read correctly check is True
        if not check:
            st.error("Không thể đọc frame từ camera. Đang thử lại...")
            continue
            
        try:
            # flip the frame for a mirror image like o/p
            frame = cv2.flip(frame, 1)
            # get landmarks & store in a list
            LmarkList = detect.findPosition(frame, draw=False)
        except Exception as e:
            st.error(f"Lỗi xử lý hình ảnh: {str(e)}")
            continue
        if len(LmarkList) != 0:
            print(LmarkList[4], LmarkList[8])

            # coordinates for landmarks of Thumb & Index fingers
            x1, y1 = LmarkList[4][1], LmarkList[4][2]
            x2, y2 = LmarkList[8][1], LmarkList[8][2]

            cv2.circle(frame, (x1, y1), 15, (0, 255, 0),
                        cv2.FILLED)  # draw circle @ thumb tip
            cv2.circle(frame, (x2, y2), 15, (0, 255, 0),
                        cv2.FILLED)  # draw circle @ index tip
            cv2.line(frame, (x1, y1), (x2, y2), (7, 0, 212), 3, 5)

            # midpt. for thumb-index joining line
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # draw circle @ midpt. of the thumb-index joing line
            cv2.circle(frame, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

            # joining line length
            length = math.hypot(x2 - x1, y2 - y1)

            # setting the volume
            # hand range : 50 to 200
            # volume range : -65 to 0
            vol = np.interp(length, [50, 300], [volMin, volMax])
            print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)

            # changing colors for respective lengths of joining line
            if length <= 50:
                cv2.circle(frame, (cx, cy), 15, (237, 250, 0),
                            cv2.FILLED)  # cyan circle

            elif length >= 200:
                cv2.circle(frame, (cx, cy), 15, (250, 0, 0),
                            cv2.FILLED)  # blue circle

        # Add instructions text to the frame
        cv2.putText(frame, "Dieu chinh volume", (25, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 0), 2)
                    
        # Update the Streamlit UI with the processed frame
        FRAME_WINDOW.image(frame, channels='BGR')
        
        # Check if we should stop (controlled by the button outside the loop)
        if st.session_state.volume_stop:
            break
            
    # Clean up resources
    video.release()
    if 'cv2' in globals():
        cv2.destroyAllWindows()
    
    # Show a message when camera is stopped
    if not st.session_state.volume_stop:
        st.session_state.volume_stop = True
        st.success("Camera đã dừng hoạt động.")
    
    # Thêm nút để bật lại camera
    if st.button("Bật lại camera", key="volume_restart_btn"):
        st.session_state.volume_stop = False
        st.session_state.volume_started = True
        st.rerun()
        
    # Uninitialize COM library when done
    comtypes.CoUninitialize()
