import math as mt
import numpy as np


parse_hex = lambda color: tuple(int(d, 16) for d in (color[1:3], color[3:5], color[5:]))
stringify_hex = lambda container: '#%02x%02x%02x' % container

clamp = lambda value, lower, upper: max(lower, min(upper, value))
color_digit_clamp = lambda value: clamp(value, lower=0, upper=255)

mk_pyramid = lambda a, b, c, d: np.array([[*p, 1] for p in (a, b, c, d)])


def color_iterator(steps: int, start: str, end: str):
  steps_count = steps // 2
  rs, gs, bs = parse_hex(start)
  re, ge, be = parse_hex(end)
  ri = mt.floor((re - rs) / steps_count)
  gi = mt.floor((ge - gs) / steps_count)
  bi = mt.floor((be - bs) / steps_count)
  colors = [(rs, gs, bs)]
  for _ in range(steps_count):
    rs = color_digit_clamp(rs + ri) 
    gs = color_digit_clamp(gs + gi) 
    bs = color_digit_clamp(bs + bi)
    colors.append((rs, gs, bs))
  colors += colors[::-1]
  yield from colors
  while True: yield colors[-1]
