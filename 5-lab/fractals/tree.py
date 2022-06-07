import math as mt


def fractal_tree(x: float, y: float, d: float, g: float, depth: float) -> list[tuple[tuple[float, ...], ...]]:
  lines = list()
  __draw_branch(x, y, d, g, depth, lines)
  return lines


def __draw_branch(x, y, d, g, depth, lines):
  x_next = x + mt.cos(g) * d
  y_next = y + mt.sin(g) * d
  lines.append(((x, y), (x_next, y_next)))
  next_params = dict(
    x=x_next,
    y=y_next,
    d=d * .8,
    depth=depth - 1,
    lines=lines,
  )
  if depth > 0:
    __draw_branch(**next_params, g=g + mt.radians(20))
    __draw_branch(**next_params, g=g - mt.radians(20))
