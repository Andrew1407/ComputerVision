import math as mt
from graphics import *
from fractals import sierpinski_carpet, fractal_tree


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

def draw_sky(wnd):
  wnd.setBackground('#a4d1f7')


def draw_lines(wnd, mtx, offset):
  fill_color = '#aa6600'
  offset_x, offset_y = offset
  for y in range(len(mtx)):
    for x in range(len(mtx[0])):
      if mtx[y, x] == 0: continue
      xi = x + offset_x
      yi = y + offset_y
      if 0 > xi > WINDOW_WIDTH or 0 > yi > WINDOW_HEIGHT:
        continue
      p = Point(xi, yi)
      p.setFill(fill_color)
      p.draw(wnd)


def draw_trees(x, y):
  lines = fractal_tree(x=x, y=y, d=20, g=mt.radians(270), depth=10)
  for start, end in lines:
    x1, y1 = start
    x2, y2 = end
    line = Line(Point(x1, y1), Point(x2, y2))
    line.setOutline('green')
    line.draw(wnd)


def draw_ground(wnd):
  level = 5
  size = 3 ** level
  mtx = sierpinski_carpet(level, size)
  mtx_height = WINDOW_HEIGHT - len(mtx)
  mtx_width = len(mtx[0])

  p1 = Point(0, mtx_height)
  p2 = Point(0, WINDOW_HEIGHT)
  p3 = Point(WINDOW_WIDTH, WINDOW_HEIGHT)
  p4 = Point(WINDOW_WIDTH, mtx_height)
  sky = Polygon(p1, p2, p3, p4)
  sky.setFill('#76b81b')
  sky.draw(wnd)
  tree_position = WINDOW_WIDTH / 4
  for i in range(3):
    draw_lines(wnd, mtx, (i * mtx_width, mtx_height))
    draw_trees(x=tree_position * (i + 1), y=mtx_height)


if __name__ == '__main__':
  wnd = GraphWin('Fractal field', WINDOW_WIDTH, WINDOW_HEIGHT)
  draw_sky(wnd)
  draw_ground(wnd)
  wnd.getMouse()
  wnd.close()
