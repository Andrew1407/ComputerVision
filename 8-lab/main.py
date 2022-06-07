from os import path
import cv2
import matplotlib.pyplot as plt
from segmentation import otsu, kmeans, robert

IMG_DIR = 'imgs'
IMG_RAW = path.join(IMG_DIR, 'raw1.png')
IMG_REF = path.join(IMG_DIR, 'ref1.png')

def write_img(img_path, name, data):
  if name == 'original': return
  format_division = img_path.rindex('.')
  img_format = img_path[format_division:]
  fullname = '{}.{}{}'.format(img_path[:format_division], name, img_format)
  cv2.imwrite(fullname, data)
  

def original(img):
  return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def apply_segms(img_path):
  img = cv2.imread(img_path)
  pos = 221
  for fn in (original, otsu, kmeans, robert):
    plt.subplot(pos)
    label = fn.__name__
    segmented = fn(img)
    cmap = None if label == 'original' else 'gray'
    plt.imshow(segmented, cmap)
    plt.title(label)
    plt.axis('off')
    pos += 1
    write_img(img_path, label, segmented)


if __name__ == '__main__':
  apply_segms(IMG_RAW)
  plt.figure()
  apply_segms(IMG_REF)
  plt.show()
