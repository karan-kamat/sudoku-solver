import numpy as np
import cv2
import pytesseract
import solve
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
char_size = 35


def is_full_white(img):
    return np.sum(img)/(char_size*char_size) == 255


def get_grid(sudoku, size):
    xf, yf = char_size, char_size
    grid = [[None for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            image = sudoku[xf*i:xf*(i+1), yf*j:yf*(j+1)]
            grid[i][j] = image
    return grid


def clean(img):
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    show_image(img)
    binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    binary_image = 255-binary_image
    show_image(binary_image)
    return binary_image


def show_image(img):
    cv2.imshow("x", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def which_number(img):
    if is_full_white(img):
        return None
    configuration = '--psm 10 tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(img, config=configuration, lang='eng',)
    if text == 's' or text == 'S':
        text = '5'
    elif text == 'I' or text == 'l':
        text = '1'
    elif text == 'O' or text == 'o':
        text = '0'
    return text


def remove_boxes(image):
    kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    temp1 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel_vertical)
    show_image(temp1)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    temp2 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, horizontal_kernel)
    show_image(temp2)
    temp3 = cv2.add(temp1, temp2)
    show_image(temp3)
    removed = cv2.add(temp3, image)
    show_image(removed)
    return removed


def main(sudoku_img):
    size = 9
    a = np.full((size, size), -1, dtype='int8')
    m, n = 0, 0
    # sudoku_img = clean(sudoku_img)
    show_image(sudoku_img)
    sudoku_img = remove_boxes(sudoku_img)
    # sudoku_img = cv2.GaussianBlur(sudoku_img, (7, 7), 0)
    show_image(sudoku_img)
    sudoku_img = 255-cv2.threshold(sudoku_img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    sudoku_img = cv2.resize(sudoku_img, (char_size*size, char_size*size))
    show_image(sudoku_img)
    grid = get_grid(sudoku_img, size)
    for i in range(9):
        for j in range(9):
            img = grid[i][j]
            x = which_number(img)
            if x is not None:
                for xi in x:
                    if '0' <= xi <= '9':
                        a[i][j] = int(xi)
    print(a)
    return a


if __name__ == '__main__':
    cor = 0
    a = main(cv2.imread(f"sudoku72.jpg"))
    sdk = solve.sudoku(9)
    sdk.a = a
    solve.main(sdk)
