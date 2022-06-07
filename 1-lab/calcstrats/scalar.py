import math as mt
from .calc_strategy import CalcStrategy


class ScalarStrategy(CalcStrategy):
  def move(self, coords: tuple[float, float], offset: tuple[float, float]) -> tuple[float, float]:
    x, y = coords
    xo, yo = offset
    return x + xo, y + yo


  def rotate(self, coords: tuple[float, float], angle: float, inverse: bool = False) -> tuple[float, float]:
    x, y = coords
    r_angle = angle if not inverse else -angle
    r_cos = mt.cos(r_angle)
    r_sin = mt.sin(r_angle)
    r_x = x * r_cos - y * r_sin
    r_y = x * r_sin + y * r_cos
    return r_x, r_y
