import cv2
import numpy as np

def adj_gamma(img, gamma=1):
    invGamma = 1.0 / gamma
    table = np.array([((i/255)**invGamma)*255 for i in np.arange(0,256)])
    lut  = cv2.LUT(img.astype(np.uint8), table.astype(np.uint8))
    return lut

def main():
    img = cv2.imread("grr3.jpg")
    if img is None:
        print("No image")
        return

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # sbx = cv2.Sobel(img, cv2.CV_64F, 1, 0,  ksize=5)
    # sby = cv2.Sobel(img, cv2.CV_64F, 0, 1,  ksize=5)
    # laplacian = cv2.Laplacian(img, cv2.CV_64F)
    # cv2.imshow('sobelx',sbx)
    # cv2.imshow('sobely',sby)
    # cv2.imshow('laplacian',laplacian)

    threshold = 130
    ksize = 21
    sigmaX = 9
    gamma = 0.1
    gblur = cv2.GaussianBlur(img, (ksize, ksize), sigmaX)
    div = cv2.divide(img, gblur, scale = 256)
    sketch = adj_gamma(div, gamma)
    ret, thresh1 = cv2.threshold(sketch, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresh1', thresh1)
    # cv2.imshow('div', div)
    # cv2.imshow('gblur', gblur)
    # cv2.imshow('sketch', sketch)

    neg = 255 - img
    gblur = cv2.GaussianBlur(neg, (ksize,ksize), 0)
    neg_blur = 255 - gblur
    sketch = cv2.divide(img, neg_blur, scale=256)
    ret, thresh2 = cv2.threshold(sketch, threshold, 255, cv2.THRESH_BINARY)
    ret, thresh_inv = cv2.threshold(sketch, threshold, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh2', thresh2)
    # cv2.imshow('thresh_inv', thresh_inv)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()