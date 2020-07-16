import solve
import numpy as np
from read import show_image, char_size
import cv2
char_size = 53


def main(img, old_a, solved_a):
    size = 9
    print(img.shape)
    print(old_a)
    print(solved_a)
    for i in range(9):
        for j in range(9):
            if old_a[i][j] == -1:
                bot_left_square = (53*(j)+10+5, 53*(i+1)-15)
                cv2.putText(img, str(solved_a[i][j]), bot_left_square,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    show_image(img)


if __name__ == '__main__':
    img = cv2.imread("sudoku52.jpg")
    img = cv2.resize(img, (480, 480))
    print(img.shape)
    old = solve.test_data1()
    oldc = np.copy(old.a)
    solved_a = solve.main(old)
    main(img, oldc, solved_a)
