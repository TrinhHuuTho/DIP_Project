import numpy as np
import cv2

L = 256

def Spectrum(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    # Bước 1 và 2: Tạo ảnh mới có kích thước PxQ và thêm số 0
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = imgin
    fp = fp / (L - 1)

    # Bước 3: Nhân (-1)^(x+y) để dời vào tâm ảnh
    for x in range(M):
        for y in range(N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]

    # Bước 4: Tính DFT
    F = cv2.dft(fp, flags=cv2.DFT_COMPLEX_OUTPUT)

    # Tính spectrum
    S = np.sqrt(F[:, :, 0]**2 + F[:, :, 1]**2)
    S = np.log1p(S)  # Sử dụng log để tăng khả năng hiển thị
    S = cv2.normalize(S, None, 0, 255, cv2.NORM_MINMAX)
    S = S.astype(np.uint8)
    return S

def FrequencyFilter(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    # Bước 1 và 2: Tạo ảnh mới có kích thước PxQ và thêm số 0
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = imgin

    # Bước 3: Nhân (-1)^(x+y) để dời vào tâm ảnh
    for x in range(M):
        for y in range(N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]

    # Bước 4: Tính DFT
    F = cv2.dft(fp, flags=cv2.DFT_COMPLEX_OUTPUT)

    # Bước 5: Tạo bộ lọc High Pass Butterworth
    H = np.zeros((P, Q), np.float32)
    D0 = 60
    n = 2
    u, v = np.meshgrid(np.arange(Q), np.arange(P))
    Duv = np.sqrt((u - Q//2)**2 + (v - P//2)**2)
    H = 1.0 / (1.0 + np.power(D0 / (Duv + 1e-10), 2 * n))

    # Bước 6: G = F * H
    G = F.copy()
    G[:, :, 0] = F[:, :, 0] * H
    G[:, :, 1] = F[:, :, 1] * H
    
    # Bước 7: IDFT
    g = cv2.idft(G, flags=cv2.DFT_SCALE)
    gp = g[:, :, 0]  # Lấy phần thực
    
    # Nhân (-1)^(x+y)
    for x in range(P):
        for y in range(Q):
            if (x + y) % 2 == 1:
                gp[x, y] = -gp[x, y]

    # Bước 8: Lấy kích thước ảnh ban đầu
    imgout = gp[:M, :N]
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def CreateNotchRejectFilter(P=250, Q=180):
    u1, v1 = 44, 58
    u2, v2 = 40, 119
    u3, v3 = 86, 59
    u4, v4 = 82, 119
    D0 = 10
    n = 2
    H = np.ones((P, Q), np.float32)

    u, v = np.meshgrid(np.arange(Q), np.arange(P))
    points = [(u1, v1), (u2, v2), (u3, v3), (u4, v4)]
    
    for u_point, v_point in points:
        # Bộ lọc cho điểm (u_point, v_point)
        Duv = np.sqrt((u - u_point)**2 + (v - v_point)**2)
        H *= 1.0 / (1.0 + np.power(D0 / (Duv + 1e-10), 2 * n))
        # Bộ lọc cho điểm đối xứng qua tâm
        Duv = np.sqrt((u - (P - u_point))**2 + (v - (Q - v_point))**2)
        H *= 1.0 / (1.0 + np.power(D0 / (Duv + 1e-10), 2 * n))

    return H

def DrawNotchRejectFilter():
    H = CreateNotchRejectFilter()
    H = H * (L - 1)
    H = H.astype(np.uint8)
    return H

def RemoveMoire(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    # Bước 1 và 2: Tạo ảnh mới có kích thước PxQ và thêm số 0
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = imgin

    # Bước 3: Nhân (-1)^(x+y) để dời vào tâm ảnh
    for x in range(M):
        for y in range(N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]

    # Bước 4: Tính DFT
    F = cv2.dft(fp, flags=cv2.DFT_COMPLEX_OUTPUT)

    # Bước 5: Tạo bộ lọc NotchReject
    H = CreateNotchRejectFilter(P, Q)

    # Bước 6: G = F * H
    G = F.copy()
    G[:, :, 0] = F[:, :, 0] * H
    G[:, :, 1] = F[:, :, 1] * H
    
    # Bước 7: IDFT
    g = cv2.idft(G, flags=cv2.DFT_SCALE)
    gp = g[:, :, 0]  # Lấy phần thực
    
    # Nhân (-1)^(x+y)
    for x in range(P):
        for y in range(Q):
            if (x + y) % 2 == 1:
                gp[x, y] = -gp[x, y]

    # Bước 8: Lấy kích thước ảnh ban đầu
    imgout = gp[:M, :N]
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout