def vertical_intersection(start: tuple[float, float], end: tuple[float, float], step: float = 1) -> tuple[tuple[float, float], ...]:
  xs, ys = start
  xe, ye = end
  y = ys
  intersected = list()
  while y < ye:
    x = xs + (ys - y) * (xe - xs) / (ys - ye)
    intersected.append((round(x), round(y)))
    y += step

  return tuple(intersected)
