def bresenhaim_line(start: tuple[float, float], end: tuple[float, float]) -> tuple[tuple[float, float], ...]:
  x1, y1 = start
  x2, y2 = end
  dx = x2 - x1
  dy = y2 - y1
  sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
  sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
  if dx < 0: dx = -dx
  if dy < 0: dy = -dy
  if dx > dy:
      pdx, pdy = sign_x, 0
      es, el = dy, dx
  else:
      pdx, pdy = 0, sign_y
      es, el = dx, dy
  x, y = x1, y1
  error, t = el / 2, 0
  points = list()
  while t < el:
      error -= es
      if error < 0:
          error += el
          x += sign_x
          y += sign_y
      else:
          x += pdx
          y += pdy
      points.append((x, y))
      t += 1
  return points
