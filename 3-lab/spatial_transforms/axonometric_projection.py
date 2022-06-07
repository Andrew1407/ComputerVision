from typing import Iterable
import math as mt
import numpy as np


__parser = lambda mtx: tuple(tuple(r[:2]) for r in mtx)

def axonometric_projection(figure: np.ndarray, angles=tuple[float, ...], parse: bool = False) -> Iterable:
  angle_first, angle_second = angles
  cos_first = mt.cos(angle_first)
  sin_first = mt.sin(angle_first)
  cos_second = mt.cos(angle_second)
  sin_second = mt.sin(angle_second)
  mtx_first = np.array([
    [cos_first, 0, -sin_first, 0],
    [0, 1, 0, 0],
    [sin_first, 0, cos_first, 0],
    [0, 0, 0, 0],
  ])
  mtx_second = np.array([
    [1, 0, 0, 0],
    [0, cos_second, sin_second, 0],
    [0, sin_second, cos_second, 0],
    [0, 0, 0, 0],
  ])
  transformer = lambda coords: coords.dot(mtx_first).dot(mtx_second)
  transformed = np.round(np.array([transformer(r) for r in figure]), decimals=2)
  return __parser(transformed) if parse else transformed
