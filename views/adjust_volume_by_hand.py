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
    # Initialize COM library before accessing audio devices
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
    
    # Page title
    st.markdown("# Điều khiển volume bằng cử chỉ ")
    FRAME_WINDOW = st.image([])
        # turn on the camera (0) 7 start capture
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setting the captured video's dimensions
    # wCam, hCam = 1920, 1080
    # video.set(3, wCam)
    # video.set(4, hCam)

    detect = htm.handDetector()  # make an object for hand detection module

    while True:
        check, frame = video.read()  # check & capture the frame
        # flip the frame for a mirror image like o/p
        frame = cv2.flip(frame, 1)
        # get landmarks & store in a list
        LmarkList = detect.findPosition(frame, draw=False)
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

        cv2.putText(frame, "Press 'q' to exit", (25, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)  # display quit key on o/p window
        cv2.imshow('=== Hand Gesture Volume Controller ===',
                    frame)  # open window for showing the o/p

        # escape key (q)
        if cv2.waitKey(1) == ord('q'):
            break
        FRAME_WINDOW.image(frame, channels='BGR')
    video.release()
    cv2.destroyAllWindows()
    
    # Uninitialize COM library when done
    comtypes.CoUninitialize()
