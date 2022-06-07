import numpy as np


def sierpinski_carpet(level: int, size: int) -> np.ndarray:
  carpet_mtx = np.ones((size, size), np.int0)
  for i in range(0, level + 1):
    stepdown = 3 ** (level - i)
    range_finish = 3 ** i
    for x in range(0, range_finish):
      if x % 3 == 1:
        for y in range(0, range_finish):
          if y % 3 == 1:
            carpet_mtx[y * stepdown : (y + 1) * stepdown, x * stepdown : (x + 1) * stepdown] = 0
  return carpet_mtx
