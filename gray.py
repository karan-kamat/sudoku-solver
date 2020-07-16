import cv2
from read import show_image
i = cv2.imread("img.jpg")
show_image(i)
g = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
show_image(g)
t = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
show_image(t)
