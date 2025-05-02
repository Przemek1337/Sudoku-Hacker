from skimage.morphology import remove_small_objects
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_mask(image, itr=0):
    image = image.copy()
    blur = cv2.GaussianBlur(image, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    thresh = cv2.dilate(thresh, np.ones([3, 3]), iterations=itr)
    thresh = cv2.erode(thresh, np.ones([3, 3]), iterations=itr)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c += 1

    mask = np.zeros((image.shape), np.uint8)
    cv2.drawContours(mask, [best_cnt], 0, 255, -1)
    cv2.drawContours(mask, [best_cnt], 0, 0, 2)

    sharpened = image.copy()
    sharpened = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)

    return mask, sharpened

def get_best_mask(image):
    maxi = 0
    for i in range(1, 4):
        hull = []
        mask, sharp = get_mask(image, i)
        for x in range(mask.shape[0]):
            for y in range(mask.shape[1]):
                if mask[x][y]:
                    hull.append([x, y])
        mina = cv2.minAreaRect(np.array(hull).copy())
        points = cv2.boxPoints(mina)
        ratio = np.array(mask == 255).sum() / cv2.contourArea(points)
        if ratio > maxi:
            maxi = ratio
            res_mask = mask
            sharpened = sharp

    return res_mask

def get_corners(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    output = np.zeros_like(mask)

    if len(contours) != 0:
        epsilon = 0.05 * cv2.arcLength(contours[0], True)
        approx = cv2.approxPolyDP(contours[0], epsilon, True)
        cv2.drawContours(output, approx, -1, 255, 3)

    corners = cv2.goodFeaturesToTrack(output, 4, 0.5, 200)
    corners = corners.squeeze()
    corners = sorted(corners, key=lambda k: [k[0], k[1]])
    corners[:2] = sorted(corners[:2], key=lambda k: [k[1], k[0]], reverse=True)
    corners[2:] = sorted(corners[2:], key=lambda k: [k[1], k[0]])
    corners = np.array(corners)

    A, D, C, B = corners.astype(np.int32)

    squares = []

    return A, B, C, D

def get_squares(corners):
    A, B, C, D = corners
    squares = []
    for y in range(9):
        for x in reversed(range(9)):
            lv0 = A * y // 9 + D * (9 - y) // 9
            rv0 = B * y // 9 + C * (9 - y) // 9

            a = lv0 * x // 9 + rv0 * (9 - x) // 9
            b = lv0 * (x + 1) // 9 + rv0 * (9 - (x + 1)) // 9

            lv1 = A * (y + 1) // 9 + D * (9 - (y + 1)) // 9
            rv1 = B * (y + 1) // 9 + C * (9 - (y + 1)) // 9

            d = lv1 * x // 9 + rv1 * (9 - x) // 9
            c = lv1 * (x + 1) // 9 + rv1 * (9 - (x + 1)) // 9

            pts = np.array([a, b, c, d])
            squares.append(pts)

    return squares

def put_intersection_dots(image, squares):
    for square in squares:
        for pt in square:
            cv2.circle(image, (pt[0], pt[1]), 8, (255), -1)

def plot_images(images, columns, rows, figsize=(20, 15), labels=None):
    fig = plt.figure(figsize=figsize)
    ax = []

    for i in range(columns * rows):
        if i >= len(images):
            break

        ax.append(fig.add_subplot(rows, columns, i + 1))
        img = images[i]

        if labels is not None and i < len(labels):
            label = labels[i]
            if isinstance(label, torch.Tensor):
                label = str(label.item())
            else:
                label = str(label)
            ax[-1].set_title(label)

        plt.imshow(img, cmap='gray')

    plt.show()

def perspective_transform(image, corners):
    def order_corner_points(corners):
        corners = [(corner[0], corner[1]) for corner in corners]
        top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
        return (top_l, top_r, bottom_r, bottom_l)

    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                           [0, height - 1]], dtype="float32")

    ordered_corners = np.array(ordered_corners, dtype="float32")

    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    return cv2.warpPerspective(image, matrix, (width, height))

def correct_squares(image, squares):
    images = []
    for square in squares:
        corrected = perspective_transform(image, square)
        corrected = cv2.adaptiveThreshold(corrected, 255, 1, 1, 11, 2)

        corrected_mask = corrected > 60
        corrected_mask = remove_small_objects(corrected_mask, 20).astype(np.int32)
        corrected[corrected_mask == 0] = 0
        corrected = cv2.resize(corrected, (28, 28))

        corrected[:5] = 0
        corrected[-5:] = 0
        corrected[:, :5] = 0
        corrected[:, -5:] = 0

        images.append(corrected)
    return images