import math as mt
from typing import Callable
from typing_extensions import Self
import numpy as np
from .calc_strategy import CalcStrategy


class MatrixComposedStrategy(CalcStrategy):
  def __init__(self):
    super().__init__()
    self.__composer: Callable[[np.ndarray], np.ndarray] = None


  def apply(self, coords: np.ndarray) -> np.ndarray:
    if not self.__composer: return coords
    result = self.__composer(coords)
    self.__composer = None
    return result


  def move(self, offset: np.ndarray) -> Self:
    prev = self.__composer
    self.__composer = lambda xy: self.__movement_action(prev(xy) if prev else xy, offset)
    return self
      


  def rotate(self, angle: float, inverse: bool = False) -> Self:
    prev = self.__composer
    self.__composer = lambda xy: self.__rotation_action(prev(xy) if prev else xy, angle, inverse)
    return self


  def __movement_action(self, coords: np.ndarray, offset: np.ndarray) -> np.ndarray:
    return coords.dot(offset)


  def __rotation_action(self, coords: np.ndarray, angle: float, inverse: bool = False) -> np.ndarray:
    r_angle = angle if not inverse else -angle
    r_cos = mt.cos(r_angle)
    r_sin = mt.sin(r_angle)
    r_mtx = np.array([
      [r_cos, r_sin, 0],
      [-r_sin, r_cos, 0],
      [0, 0, 1]
    ])
    return coords.dot(r_mtx)
