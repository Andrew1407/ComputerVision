import math as mt
from graphics import *
from drawing import stringify_hex, mk_pyramid, color_iterator
from raster import bresenhaim_line, vertical_intersection, get_contour_lines
from spatial_transforms import axonometric_projection


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

PROJECTION_ANGLES = 1, -0.1
STEPS = 50

BACKGROUND_COLOR = '#ffff00'

FIRST_OUTLINE_COLOR = '#ff0000'
SECOND_OUTLINE_COLOR = '#19507b'

FIRST_FILL_COLOR = '#11ccee'
SECOND_FILL_COLOR = '#eaccff'

def draw_bkg(components, color_gen):
  for triangle in components:
    t_sorted = sorted(triangle, key=lambda xy: xy[1])
    i = 1
    contours = list()
    while i < len(t_sorted):
      prev = t_sorted[i - 1]
      cur = t_sorted[i]
      cntr = vertical_intersection(start=prev, end=cur)
      contours += list(cntr)
      i += 1
    contours += list(vertical_intersection(start=t_sorted[0], end=t_sorted[-1]))
    lines = get_contour_lines(contours)
    for p1, p2 in lines:
      points = bresenhaim_line(start=p2, end=p1)
      steps = 2 if len(points) < 2 else len(points)
      bkg_clr = color_gen(steps)
      for x, y in points:
        p = Point(x, y)
        p.setFill(stringify_hex(next(bkg_clr)))
        p.draw(wnd)


def draw_lines(components, color_gen):
  for triangle in components:
    i = 0
    while i < len(triangle):
      p1 = triangle[i]
      p2 = triangle[i + 1] if i < len(triangle) - 1 else triangle[0]
      points = bresenhaim_line(start=p1, end=p2)
      steps = 2 if len(points) < 2 else len(points)
      line_clr = color_gen(steps)
      for x, y in points:
        p = Point(x, y)
        p.setFill(stringify_hex(next(line_clr)))
        p.draw(wnd)
      i += 1


if __name__ == '__main__':
  pyramid = mk_pyramid(
    a=(720, 300, 10),
    b=(680, 300, 80),
    c=(770, 350, 80),
    d=(700, 200, 50)
  )
  projection = axonometric_projection(pyramid, PROJECTION_ANGLES, parse=True)
  a, b, c, d = projection
  components = (a, b, c), (a, c, d), (a, b, d), (b, c, d)
  color_params = (
    dict(
      bkg=dict(start=FIRST_FILL_COLOR, end=SECOND_FILL_COLOR),
      lines=dict(start=FIRST_OUTLINE_COLOR, end=SECOND_OUTLINE_COLOR),
    ),
    dict(
      bkg=dict(start=SECOND_FILL_COLOR, end=FIRST_FILL_COLOR),
      lines=dict(start=SECOND_OUTLINE_COLOR, end=FIRST_OUTLINE_COLOR),
    ),
    dict(
      bkg=dict(start=BACKGROUND_COLOR, end=BACKGROUND_COLOR),
      lines=dict(start=BACKGROUND_COLOR, end=BACKGROUND_COLOR),
    ),
  )

  wnd = GraphWin('3D raster animation', WINDOW_WIDTH, WINDOW_HEIGHT)
  wnd.setBackground(BACKGROUND_COLOR)
  for params in color_params:
    bkg = params['bkg']
    lines = params['lines']
    bkg_colors = lambda steps: color_iterator(steps=steps, **bkg)
    lines_colors = lambda steps: color_iterator(steps=steps, **lines)
    draw_bkg(components, bkg_colors)
    draw_lines(components, lines_colors)
  wnd.getMouse()
  wnd.close()
