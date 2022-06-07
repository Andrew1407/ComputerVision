import numpy as np
import cv2
from scipy import ndimage


def robert(img):
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  imgf = img_gray.astype('float64') / 255
  vertical = ndimage.convolve(imgf, np.array([[1, 0], [0, -1]]))
  horizontal = ndimage.convolve(imgf, np.array([[0, 1], [-1, 0]]))
  edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))
  return edged_img * 255


def otsu(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
  return thresh


def kmeans(img):
  k = 2
  attempts = 10
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)

  img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  twoDimage = np.float32(img_cvt.reshape((-1, 3)))
  _, label, center = cv2.kmeans(twoDimage, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
  center = np.uint8(center)
  return center[label.flatten()].reshape(img_cvt.shape)

