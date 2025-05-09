import numpy as np
import cv2

L = 256

def Negative(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            s = L - 1 - r
            imgout[x, y] = s
    return imgout

def Logarit(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    c = (L - 1) / np.log(L)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            if r == 0:
                r = 1
            s = c * np.log(1 + r)
            imgout[x, y] = np.uint8(s)
    return imgout

def Power(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    gamma = 5.0
    c = np.power(L - 1, 1 - gamma)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            s = c * np.power(r, gamma)
            imgout[x, y] = np.uint8(s)
    return imgout

def PiecewiseLinear(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    rmin, rmax, _, _ = cv2.minMaxLoc(imgin)
    r1 = rmin
    s1 = 0
    r2 = rmax
    s2 = L - 1
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            if r < r1:
                s = s1 / r1 * r if r1 != 0 else 0
            elif r < r2:
                s = (s2 - s1) / (r2 - r1) * (r - r1) + s1 if r2 != r1 else s1
            else:
                s = (L - 1 - s2) / (L - 1 - r2) * (r - r2) + s2 if r2 != L - 1 else s2
            imgout[x, y] = np.uint8(s)
    return imgout

def Histogram(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, L), np.uint8) + 255
    h = np.zeros(L, np.int32)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            h[r] += 1
    p = h / (M * N)
    scale = 2000
    for r in range(L):
        cv2.line(imgout, (r, M - 1), (r, M - 1 - int(scale * p[r])), (0, 0, 0))
    return imgout

def HistEqual(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    h = np.zeros(L, np.int32)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            h[r] += 1
    p = h / (M * N)
    s = np.zeros(L, np.float64)
    for k in range(L):
        s[k] = np.sum(p[:k + 1])
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            imgout[x, y] = np.uint8((L - 1) * s[r])
    return imgout

def HistEqualColor(imgin):
    if len(imgin.shape) != 3:  # Ảnh xám
        raise ValueError("HistEqualColor requires a color image (3 channels)")
    B, G, R = cv2.split(imgin)
    B = cv2.equalizeHist(B)
    G = cv2.equalizeHist(G)
    R = cv2.equalizeHist(R)
    imgout = cv2.merge((B, G, R))
    return imgout

def LocalHist(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    for x in range(a, M - a):
        for y in range(b, N - b):
            w = imgin[x - a:x + a + 1, y - b:y + b + 1]
            w_eq = cv2.equalizeHist(w)
            imgout[x, y] = w_eq[a, b]
    return imgout

def HistStat(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    mG, sigmaG = cv2.meanStdDev(imgin)
    mG = mG[0][0]
    sigmaG = sigmaG[0][0]
    C = 22.8
    k0 = 0.0
    k1 = 0.1
    k2 = 0.0
    k3 = 0.1
    for x in range(a, M - a):
        for y in range(b, N - b):
            w = imgin[x - a:x + a + 1, y - b:y + b + 1]
            msxy, sigmasxy = cv2.meanStdDev(w)
            msxy = msxy[0][0]
            sigmasxy = sigmasxy[0][0]
            r = imgin[x, y]
            if (k0 * mG <= msxy <= k1 * mG) and (k2 * sigmaG <= sigmasxy <= k3 * sigmaG):
                imgout[x, y] = np.uint8(C * r)
            else:
                imgout[x, y] = r
    return imgout

def MyBoxFilter(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 11
    n = 11
    w = np.ones((m, n)) / (m * n)
    a = m // 2
    b = n // 2
    for x in range(a, M - a):
        for y in range(b, N - b):
            r = np.sum(w * imgin[x - a:x + a + 1, y - b:y + b + 1])
            imgout[x, y] = np.uint8(r)
    return imgout

def BoxFilter(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    m = 21
    n = 21
    w = np.ones((m, n)) / (m * n)
    imgout = cv2.filter2D(imgin, cv2.CV_8UC1, w)
    return imgout

def Threshold(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    temp = cv2.blur(imgin, (15, 15))
    _, imgout = cv2.threshold(temp, 64, 255, cv2.THRESH_BINARY)
    return imgout

def MedianFilter(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 5
    n = 5
    a = m // 2
    b = n // 2
    for x in range(M):
        for y in range(N):
            w = imgin[max(0, x - a):min(M, x + a + 1), max(0, y - b):min(N, y + b + 1)]
            w_flat = w.flatten()
            w_flat.sort()
            imgout[x, y] = w_flat[len(w_flat) // 2]
    return imgout

def Sharpen(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    temp = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    imgout = imgin - temp
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def Gradient(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gx = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_x)
    gy = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_y)
    imgout = np.abs(gx) + np.abs(gy)
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout