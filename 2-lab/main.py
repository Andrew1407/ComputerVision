import math as mt
import time
import numpy as np
from typing import Iterable
from graphics import *
from drawing import define_drawing_layers, figure_cleanup, parse_hex, stringify_hex
from spatial_transforms import axonometric_projection, custom_rotation


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

DRAW_DELAY_SEC = .2
STEPS = 50

BACKGROUND_COLOR = '#ffff00'
OUTLINE_COLOR = '#0000ff'
FILL_START_COLOR = BACKGROUND_COLOR
FILL_FINISH_COLOR = '#ff99cc'

PROJECTION_ANGLES = mt.pi / 3, -mt.pi / 4
ROTATION_COORDS = 1, 0, 0
ROTATION_ANGLE = .02

mk_pyramid = lambda a, b, c, d: np.array([[*p, 1] for p in (a, b, c, d)])

lerp = lambda value, lower, upper: max(lower, min(upper, value))
color_digit_lerp = lambda value: lerp(value, lower=0, upper=255)


def color_iterator(steps: int, start: str, end: str):
  steps_count = steps // 2
  rs, gs, bs = parse_hex(start)
  re, ge, be = parse_hex(end)
  ri = mt.floor((re - rs) / steps_count)
  gi = mt.floor((ge - gs) / steps_count)
  bi = mt.floor((be - bs) / steps_count)
  colors = [(rs, gs, bs)]
  for _ in range(steps_count):
    rs = lerp(value=rs + ri, lower=0, upper=255)
    rs = color_digit_lerp(rs + ri) 
    gs = color_digit_lerp(gs + gi) 
    bs = color_digit_lerp(bs + bi)
    colors.append((rs, gs, bs))
  colors += colors[::-1]
  yield from colors
  while True: yield colors[-1]


def angle_rotation(angle):
  angle_i = 0
  pi2 = mt.pi * 2
  while True:
    yield angle_i
    if angle_i >= pi2: angle_i -= pi2
    angle_i += angle


def draw_shape(figure: Iterable, env: GraphWin, color_bkg: str, color_line: str):
  polygon = tuple(Point(*p) for p in figure)
  bkg, carcass = define_drawing_layers(points=polygon)
  for bkg_polygon in bkg:
    bkg_polygon.setFill(color_bkg)
    bkg_polygon.setOutline(color_bkg)
    bkg_polygon.draw(env)
  for carcass_polygon in carcass:
    carcass_polygon.setWidth(3)
    carcass_polygon.setOutline(color_line)
    carcass_polygon.draw(env)
  return bkg, carcass


def draw_animation(label, figure, transformer, projection_angles):
  pyramid=figure
  angle_gen = angle_rotation(angle=ROTATION_ANGLE)
  fill_color = color_iterator(steps=STEPS, start=FILL_START_COLOR, end=FILL_FINISH_COLOR)
  outline_color = color_iterator(steps=STEPS, start=BACKGROUND_COLOR, end=OUTLINE_COLOR)
  wnd = GraphWin(label, WINDOW_WIDTH, WINDOW_HEIGHT)
  wnd.setBackground(BACKGROUND_COLOR)
  for _ in range(STEPS):
    angle = next(angle_gen)
    fill = stringify_hex(next(fill_color))
    outline = stringify_hex(next(outline_color))
    pyramid = transformer(figure=pyramid, angle=angle, rotation_coords=ROTATION_COORDS)
    projection = axonometric_projection(pyramid, projection_angles, parse=True)
    layers = draw_shape(figure=projection, env=wnd, color_bkg=fill, color_line=outline)
    time.sleep(DRAW_DELAY_SEC)
    figure_cleanup(layers)
  wnd.getMouse()
  wnd.close()


if __name__ == '__main__':
  pyramid = mk_pyramid(
    a=(720, 300, 10),
    b=(680, 300, 80),
    c=(770, 350, 80),
    d=(700, 200, 50)
  )
  drawings = (
    dict(
      label='3D projection',
      figure=pyramid,
      transformer=lambda figure, **_: figure,
      projection_angles=(1, -0.1)
    ),
    dict(
      label='3D rotation & projection',
      figure=pyramid,
      transformer=custom_rotation,
      projection_angles=PROJECTION_ANGLES
    ),
  )
  for params in drawings: draw_animation(**params)
