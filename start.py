import cv2
import numpy as np
import read
import solve
import time
import getbox
from math import ceil
import out


def met1():
    img = cv2.imread("sudoku7.jpg")
    return img


def main(img, ispaper):
    img = getbox.main(img)
    a = read.main(img)
    a_c = np.copy(a)
    sdk = solve.sudoku(9, a)
    solved_a = solve.main(sdk)
    out.main(img, a_c, solved_a)


def met2():
    size = 35
    side = size*9
    cap = cv2.VideoCapture(0)
    x, y, c = cap.read()[1].shape
    top_b, left_b = (x-side)//2, (y-side)//2
    right_b, bottom_b = left_b+side, top_b+side
    square_side = x//6
    bot_left_square = (y-square_side, square_side-x//48)
    i = 0
    while (cap.isOpened()):
        if(i == 0):
            i += 1
            end = time.time()+20
        sec = ceil(int(end-time.time()))
        return_val, img = cap.read()
        if not return_val:
            break
        if (sec == 0):
            cv2.destroyAllWindows()
            cap.release()
            break
        img2 = np.copy(img)
        img = img//4
        img[top_b:bottom_b, left_b:right_b, :] = img2[top_b:bottom_b, left_b:right_b, :]
        img[:square_side, -1:-square_side-1:-1, :] = np.full((square_side, square_side, 3), 255)
        cv2.putText(img, str(sec), bot_left_square,
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2)
        cv2.imshow("x", img)
        k = cv2.waitKey(1)
        if k == 13:
            cv2.destroyAllWindows()
            cap.release()
            break
    img = img2[top_b:bottom_b, left_b:right_b, :]
    read.show_image(img)
    return img


if __name__ == '__main__':
    ispaper = False  # (input("Is this photo paper?(y/n)") == 'y')
    main(met2(), ispaper)
