import read
import cv2
import numpy as np


def crop(img, x, y, w, h):
    return img[x:x+h, y:y+w]


def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def main(img):
    print(img.shape)
    x, y, c = img.shape
    img = cv2.resize(img, (480, 480*y//x))
    imgc2 = np.copy(img)
    x, y, c = img.shape
    read.show_image(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    read.show_image(gray)
    img2 = cv2.GaussianBlur(gray, (5, 5), 0)
    read.show_image(img2)
    thresh = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    read.show_image(thresh)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    imgc = np.copy(img)
    cv2.drawContours(imgc, contours, -1, (0, 255, 0), 3)
    read.show_image(imgc)
    square = []
    i = 0
    max_area = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, peri*0.02, True)
            if area > max_area and len(approx) == 4:
                max_area = area
                square = approx
    square = rectify(square)
    h = np.array([[0, 0], [479, 0], [479, 479], [0, 479]], np.float32)
    retval = cv2.getPerspectiveTransform(square, h)
    warp = cv2.warpPerspective(img, retval, (480, 480))
    # cv2.imwrite("sudoku52.jpg", warp)
    read.show_image(warp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return warp


if __name__ == '__main__':
    main(cv2.imread("sudoku5.jpg"))
