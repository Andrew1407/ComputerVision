import numpy as np


def least_squares(start: tuple[float, float], end: tuple[float, float]) -> tuple[tuple[float, float], ...]:
  x1, y1 = start
  x2, y2 = end
  dx = x2 - x1;  dy = y2 - y1
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
  while t < el:
      error -= es
      if error < 0:
          error += el
          x += sign_x
          y += sign_y
      else:
          x += pdx
          y += pdy
      t += 1
  stopt = t
  Yin = np.zeros((stopt, 1))
  F = np.ones((stopt, 2))
  FX = np.ones((stopt, 2))
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
  while t < el:
      error -= es
      if error < 0:
          error += el
          x += sign_x
          y += sign_y
      else:
          x += pdx
          y += pdy
      t += 1
      tt=t-1
      Yin[tt, 0] = float(y)
      F[tt, 1] = float(x)
      FX[tt, 1] = float(x)
  for i in range (0, stopt): F[i, 1] = i
  FT = F.T
  FFT = FT.dot(F)
  FFTI = np.linalg.inv(FFT)
  FFTIFT = FFTI.dot(FT)
  C = FFTIFT.dot(Yin)
  Yout = F.dot(C)
  return tuple((FX[i, 1], Yout[i, 0]) for i in range(0, stopt))
