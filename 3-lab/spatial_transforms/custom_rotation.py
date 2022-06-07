import numpy as np
import math as mt


def __generate_rotation_matrix(angle: float, rotation_coords: tuple[float, ...]) -> np.ndarray:
  angle_cos = mt.cos(angle)
  angle_sin = mt.sin(angle)
  direction_param = mt.sqrt(sum(rotation_coords))
  n1, n2, n3 = tuple(p / direction_param for p in rotation_coords)
  n1_pow, n2_pow, n3_pow = tuple(p ** 2 for p in (n1, n2, n3))
  n1n2 = n1 * n2
  n1n3 = n1 * n3
  n2n3 = n2 * n3
  return np.array([
    [n1_pow + (1 - n1_pow) * angle_cos, n1n2 * (1 - angle_cos) + n3 * angle_sin, n1n3 * (1 - angle_cos) + n2 * angle_sin, 0],
    [n1n2 * (1 - angle_cos) - n3 * angle_sin, n2_pow + (1 - n2_pow) * angle_cos, n2n3 * (1 - angle_cos) + n1 * angle_sin, 0],
    [n1n3 * (1 - angle_cos) + n2 * angle_sin, n2n3 * (1 - angle_cos) - n1 * angle_sin, n3_pow + (1 - n3_pow) * angle_cos, 0],
    [0, 0, 0, 1],
  ])

__generate_coords_mtx = lambda coords: np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [*coords, 1],
  ])


__parser = lambda mtx: tuple(tuple(r[:2]) for r in mtx)

def custom_rotation(figure: np.ndarray, angle: float, rotation_coords: tuple[float, ...], parse: bool = False) -> np.ndarray:
  r = __generate_rotation_matrix(angle, rotation_coords)
  coords_plus = __generate_coords_mtx(rotation_coords)
  coords_min = __generate_coords_mtx(tuple(-c for c in rotation_coords))
  transformer = lambda coords: (coords
    .dot(coords_min)
    .dot(r)
    .dot(coords_plus)
  )
  result = np.round(np.array([transformer(c) for c in figure]), decimals=2)
  return __parser(result) if parse else result
