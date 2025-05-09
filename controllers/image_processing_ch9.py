import cv2
import numpy as np

L = 256

def Erosion(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45))
    imgout = cv2.erode(imgin, w)
    return imgout

def Dilation(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgout = cv2.dilate(imgin, w)
    return imgout

def OpeningClosing(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_OPEN, w)
    imgout = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, w)
    return imgout

def Boundary(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    temp = cv2.erode(imgin, w)
    imgout = imgin - temp
    return imgout

def HoleFill(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    imgout = imgin.copy()
    M, N = imgout.shape
    mask = np.zeros((M + 2, N + 2), np.uint8)
    cv2.floodFill(imgout, mask, (105, 297), L - 1)
    return imgout

def MyConnectedComponent(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    ret, temp = cv2.threshold(imgin, 200, L - 1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    M, N = temp.shape
    dem = 0
    color = 150
    for x in range(M):
        for y in range(N):
            if temp[x, y] == L - 1:
                mask = np.zeros((M + 2, N + 2), np.uint8)
                cv2.floodFill(temp, mask, (y, x), (color, color, color))
                dem += 1
                color += 1
    print(f'Có {dem} thành phần liên thông')
    a = np.zeros(L, np.int32)
    for x in range(M):
        for y in range(N):
            r = temp[x, y]
            if r > 0:
                a[r] += 1
    dem = 1
    for r in range(L):
        if a[r] > 0:
            print(f'{dem:4d}   {a[r]:5d}')
            dem += 1
    return temp

def ConnectedComponent(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    ret, temp = cv2.threshold(imgin, 200, L - 1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    dem, label = cv2.connectedComponents(temp)
    text = f'Có {dem - 1} thành phần liên thông'

    a = np.zeros(dem, np.int32)
    M, N = label.shape
    color = 150
    for x in range(M):
        for y in range(N):
            r = label[x, y]
            a[r] += 1
            if r > 0:
                label[x, y] = label[x, y] + color

    for r in range(1, dem):
        print(f'{r:4d} {a[r]:10d}')
    label = label.astype(np.uint8)
    return text, label

def CountRice(imgin):
    if len(imgin.shape) == 3:  # Ảnh màu
        imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    w = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_TOPHAT, w)
    ret, temp = cv2.threshold(temp, 100, L - 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    temp = cv2.medianBlur(temp, 3)
    dem, label = cv2.connectedComponents(temp)
    text = f'Có {dem - 1} hạt gạo'

    a = np.zeros(dem, np.int32)
    M, N = label.shape
    color = 150
    for x in range(M):
        for y in range(N):
            r = label[x, y]
            a[r] += 1
            if r > 0:
                label[x, y] = label[x, y] + color

    max_val = a[1]
    rmax = 1
    for r in range(2, dem):
        if a[r] > max_val:
            max_val = a[r]
            rmax = r

    xoa = np.array([], np.int32)
    for r in range(1, dem):
        if a[r] < 0.5 * max_val:
            xoa = np.append(xoa, r)

    for x in range(M):
        for y in range(N):
            r = label[x, y]
            if r > 0:
                r = r - color
                if r in xoa:
                    label[x, y] = 0

    label = label.astype(np.uint8)
    return text, label