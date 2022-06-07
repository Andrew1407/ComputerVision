import math as mt
import numpy as np
from .calc_strategy import CalcStrategy


class MatrixSequentialStrategy(CalcStrategy):
  def move(self, coords: np.ndarray, offset: np.ndarray) -> np.ndarray:
    return coords + offset


  def rotate(self, coords: np.ndarray, angle: float, inverse: bool = False) -> np.ndarray:
    r_angle = angle if not inverse else -angle
    r_cos = mt.cos(r_angle)
    r_sin = mt.sin(r_angle)
    r_mtx = np.array([
      [r_cos, r_sin],
      [-r_sin, r_cos]
    ])
    return coords.dot(r_mtx)
