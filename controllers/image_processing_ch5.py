import cv2
import numpy as np
from numpy.fft import fft2, ifft2
from scipy import signal
from scipy.ndimage import gaussian_filter

L = 256

def CreateMotionFilter(M, N):
    H = np.zeros((M, N), np.complex128)
    a = 0.1
    b = 0.1
    T = 1
    for u in range(M):
        for v in range(N):
            phi = np.pi * ((u - M//2) * a + (v - N//2) * b)
            if np.abs(phi) < 1.0e-6:
                RE = T * np.cos(phi)
                IM = -T * np.sin(phi)
            else:
                RE = T * np.sin(phi) / phi * np.cos(phi)
                IM = -T * np.sin(phi) / phi * np.sin(phi)
            H[u, v] = RE + 1j * IM
    return H

def CreateMotionNoise(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    f = imgin.astype(np.float64)
    
    # Bước 1: DFT
    F = fft2(f)
    
    # Bước 2: Shift vào tâm ảnh
    F = np.fft.fftshift(F)

    # Bước 3: Tạo bộ lọc H
    H = CreateMotionFilter(M, N)

    # Bước 4: Nhân F với H
    G = F * H

    # Bước 5: Shift lại
    G = np.fft.ifftshift(G)

    # Bước 6: IDFT
    g = ifft2(G)
    g = np.clip(g.real, 0, L - 1)
    g = g.astype(np.uint8)
    return g

def CreateInverseMotionFilter(M, N):
    H = np.zeros((M, N), np.complex128)
    a = 0.1
    b = 0.1
    T = 1
    phi_prev = 0
    for u in range(M):
        for v in range(N):
            phi = np.pi * ((u - M//2) * a + (v - N//2) * b)
            if np.abs(phi) < 1.0e-6:
                RE = np.cos(phi) / T
                IM = np.sin(phi) / T
            else:
                if np.abs(np.sin(phi)) < 1.0e-6:
                    phi = phi_prev
                RE = phi / (T * np.sin(phi)) * np.cos(phi)
                IM = phi / (T * np.sin(phi)) * np.sin(phi)
            H[u, v] = RE + 1j * IM
            phi_prev = phi
    return H

def DenoiseMotion(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    M, N = imgin.shape
    f = imgin.astype(np.float64)
    
    # Bước 1: DFT
    F = fft2(f)
    
    # Bước 2: Shift vào tâm ảnh
    F = np.fft.fftshift(F)

    # Bước 3: Tạo bộ lọc H
    H = CreateInverseMotionFilter(M, N)

    # Bước 4: Nhân F với H
    G = F * H

    # Bước 5: Shift lại
    G = np.fft.ifftshift(G)

    # Bước 6: IDFT
    g = ifft2(G)
    g = np.clip(g.real, 0, L - 1)
    g = g.astype(np.uint8)
    return g

def gaussian_kernel(kernel_size=3):
    sigma = kernel_size / 3
    h = gaussian_filter(np.ones((kernel_size, 1)), sigma)
    h = np.dot(h, h.T)
    h /= np.sum(h)
    return h

def WienerFilter(imgin, kernel_size=3, K=10):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    kernel = gaussian_kernel(kernel_size)
    dummy = np.copy(imgin).astype(np.float64)
    kernel = np.pad(kernel, [(0, dummy.shape[0] - kernel.shape[0]), (0, dummy.shape[1] - kernel.shape[1])], 'constant')
    
    # Fourier Transform
    dummy = fft2(dummy)
    kernel = fft2(kernel)
    kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
    dummy = dummy * kernel
    dummy = np.abs(ifft2(dummy))
    dummy = np.clip(dummy, 0, L - 1)
    return dummy.astype(np.uint8)

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