import math as mt
import numpy as np


def __generate_rotation_matrix(angle: float, axis: str) -> np.ndarray:
  angle_cos = mt.cos(angle)
  angle_sin = mt.sin(angle)
  if axis == 'x': return np.array([
    [1, 0, 0, 0],
    [1, angle_cos, angle_sin, 0],
    [1, -angle_sin, angle_cos, 0],
    [0, 0, 0, 1],
  ])
  if axis == 'y': return np.array([
    [angle_cos, 0, -angle_sin, 0],
    [0, 1, 0, 0],
    [angle_sin, 0, angle_cos, 0],
    [0, 0, 0, 1],
  ])
  if axis == 'z': return np.array([
    [angle_cos, 0, angle_sin, 0],
    [angle_sin, 1, angle_cos, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
  ])
  return None


def axis_rotation(figure: np.ndarray, angle: float, axis: str) -> np.ndarray:
  rotation_mtx = __generate_rotation_matrix(axis=axis, angle=angle)
  result = np.array([coords.dot(rotation_mtx) for coords in figure])
  return np.round(result, decimals=2)
