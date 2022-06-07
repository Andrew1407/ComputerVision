import cv2
import numpy as np
from matplotlib import pyplot as plt


IMGNAME = 'imgs/landscape.jpg'


cvt_to_rgb = lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
draw_img_colored = lambda img: plt.imshow(cvt_to_rgb(img))

def draw_hist(img, mask=None):
  plt.plot(cv2.calcHist([img], [0], mask, [256], [0,256]))


def draw_subplots(*params):
  pos = 221
  for img, mask in params:
    plt.subplot(pos)
    draw_img_colored(img)
    pos += 1
    plt.subplot(pos)
    draw_hist(img, mask)
    pos += 1


def stretch_contrast(img):
  xp = [0, 64, 128, 192, 255]
  fp = [0, 64, 128, 240, 255]
  x = np.arange(256)
  table = np.interp(x, xp, fp).astype('uint8')
  return cv2.LUT(img, table)
 

if __name__ == '__main__':
  img = cv2.imread(IMGNAME)

  mask = np.zeros(img.shape[:2], np.uint8)
  mask[350:550, 300:700] = 1
  masked_img = cv2.bitwise_and(img, img, mask = mask)

  draw_subplots((img, None), (masked_img, mask))
  plt.figure()

  img_stretched = stretch_contrast(img)
  img_norm = cv2.normalize(masked_img, None, 0, 255, cv2.NORM_MINMAX)

  draw_subplots((img_stretched, None), (img_norm, mask))
  plt.show()
