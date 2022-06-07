from dataclasses import dataclass
from typing import Iterable
import numpy as np


@dataclass
class PlaneParams:
  position: int
  coords: tuple[float, float]


__PLANES_TRANSFORMS: dict[str, PlaneParams] = dict(
  xy = PlaneParams(position=2, coords=(0, 1)),
  xz = PlaneParams(position=1, coords=(0, 2)),
  yz = PlaneParams(position=0, coords=(2, 1)),
)

def __parser (values: np.ndarray, coords: tuple[float, ...]) -> tuple[tuple[float, ...], ...]:
  parsed = list()
  for row in values:
    parsed.append(tuple(row[i] for i in coords))
  return tuple(parsed)


def orthogonal_projection(figure: np.ndarray, plane: str = 'xy', parse: bool = False) -> Iterable:
  projection_mtx = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
  ])
  params = __PLANES_TRANSFORMS[plane]
  projection_mtx[params.position, params.position] = 0
  result = np.round(figure.dot(projection_mtx), decimals=2)
  return __parser(result, params.coords) if parse else result
