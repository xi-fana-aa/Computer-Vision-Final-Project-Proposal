import cv2
import numpy as np
import os

def preprocess_image(img_bytes, target_width=800, min_board_percent=0.10, save_debug=False):
    """
    入口函数：接受图片字节流，返回透视变换后的棋盘图像（np.ndarray）
    """
    nparr = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("图像解码失败")

    warped = preprocess_and_warp_from_image(image, target_width, min_board_percent, save_debug)
    return warped

def preprocess_and_warp_from_image(image, target_width=800, min_board_percent=0.10, save_debug=False):
    """
    处理 np.ndarray 类型图像，完成预处理与棋盘提取（透视变换）
    """
    h, w = image.shape[:2]
    scale = target_width / float(w)
    resized = cv2.resize(image, (target_width, int(h * scale)))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 二值化 + 形态学操作
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV,
                                   blockSize=11, C=3)
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    morphed = cv2.dilate(morphed, kernel)

    if save_debug:
        cv2.imwrite("debug_thresh.png", thresh)
        cv2.imwrite("debug_morphed.png", morphed)

    # 找轮廓并筛选面积
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_area = resized.shape[0] * resized.shape[1]
    min_area = img_area * min_board_percent
    big_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    big_contours = sorted(big_contours, key=cv2.contourArea, reverse=True)

    # 找四边形
    quad_corners = None
    for cnt in big_contours:
        peri = cv2.arcLength(cnt, True)
        for eps_coef in [0.01, 0.02, 0.03, 0.04]:
            approx = cv2.approxPolyDP(cnt, eps_coef * peri, True)
            if len(approx) == 4:
                quad_corners = approx.reshape(4, 2)
                break
        if quad_corners is not None:
            break
    if quad_corners is None:
        raise RuntimeError("未找到有效四边形轮廓")

    # 透视变换
    corners = sort_corners(quad_corners)
    warped = four_point_transform(resized, corners)
    if save_debug:
        cv2.imwrite("debug_warped.png", warped)

    return warped

def sort_corners(pts):
    pts = np.array(pts)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    return np.array([pts[np.argmin(s)], pts[np.argmin(diff)],
                     pts[np.argmax(s)], pts[np.argmax(diff)]], dtype="float32")

def four_point_transform(image, pts):
    (tl, tr, br, bl) = pts
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxSize = int(max(max(widthA, widthB), max(heightA, heightB)))

    dst = np.array([
        [0, 0],
        [maxSize - 1, 0],
        [maxSize - 1, maxSize - 1],
        [0, maxSize - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(pts, dst)
    return cv2.warpPerspective(image, M, (maxSize, maxSize))

def correct_rotation(warped, save_debug=False):
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    if save_debug:
        cv2.imwrite("debug_edges.png", edges)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    if lines is None:
        return warped  # 无旋转校正

    thetas = np.array([line[0][1] * 180 / np.pi for line in lines])
    mask = np.logical_and(thetas > -45, thetas < 45)
    angle = np.median(thetas[mask]) if np.sum(mask) else np.median(thetas)

    (h, w) = warped.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)

    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    rotated = cv2.warpAffine(warped, M, (new_w, new_h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(255, 255, 255))
    if save_debug:
        cv2.imwrite("debug_rotated.png", rotated)

    return rotated