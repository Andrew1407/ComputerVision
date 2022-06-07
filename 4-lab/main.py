import numpy as np
from graphics import *
from raster import bresenhaim_line, vertical_intersection, get_contour_lines
from spatial_transforms import orthogonal_projection
from vector import least_squares, painter_algorithm


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

BACKGROUND_COLOR = '#ffff00'
OUTLINE_COLOR = '#19507b'
FILL_COLOR = '#11ccee'

def draw_bkg(components, color):
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
      for x, y in points:
        p = Point(x, y)
        p.setFill(color)
        p.draw(wnd)


if __name__ == '__main__':
  a = (420, 350, 10)
  b = (380, 300, 80)
  c = (470, 350, 80)
  d = (400, 200, 50)
  vertices = (a, c, d), (a, b, c), (a, b, d), (b, c, d)

  vertices_ordered = painter_algorithm(vertices)
  ordered_coords = list()
  for vs in vertices_ordered:
    ordered_coords.append(np.array([[*p, 1] for p in vs]))

  projections = [orthogonal_projection(vs, plane='xy', parse=True) for vs in ordered_coords]
  wnd = GraphWin('3D vector animation', WINDOW_WIDTH, WINDOW_HEIGHT)
  wnd.setBackground(BACKGROUND_COLOR)

  for edge in projections:
    a, b, c = edge
    draw_bkg(components=(edge,), color=FILL_COLOR)
    lines = (a, b), (b, c), (a, c)
    for start, end in lines:
      points = least_squares(start, end)
      for p in points:
        x, y = p
        drawable = Point(x, y)
        drawable.setFill(OUTLINE_COLOR)
        drawable.draw(wnd)

  wnd.getMouse()
  wnd.close()
