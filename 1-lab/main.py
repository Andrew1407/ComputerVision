from typing import Iterable
from graphics import *
import time
import numpy as np
import math as mt
import calcstrats as clst


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

X1, X2 = 720, 780
Y2, Y1 = 80, 10
X_OFFSET = 20

MOVE_OFFSET = (-10, 10)
MOVE_ANGLE = mt.pi / 50
MOVE_ANGLE_INVERSE = -mt.pi / 80
MOVE_TIMES = 20

DRAW_DELAY_SEC = 0.25

strategies = dict(
  scalar = clst.ScalarStrategy,
  matrix_sequential = clst.MatrixSequentialStrategy,
  matrix_composed = clst.MatrixComposedStrategy
)


def draw_polygon(env: GraphWin, pol: Polygon):
  time.sleep(DRAW_DELAY_SEC)
  pol.setWidth(3)
  pol.setOutline('blue')
  pol.draw(env)


def points_mapper(points: Iterable, strategy: clst.CalcStrategy, offset: Iterable):
  results = []
  composed = isinstance(strategy, clst.MatrixComposedStrategy)
  for p in points:
    res = None
    if composed:
      res = (strategy
        .move(offset=offset)
        .rotate(angle=MOVE_ANGLE, inverse=False)
        .rotate(angle=MOVE_ANGLE_INVERSE, inverse=True)
        .apply(p))
    else: 
      res = strategy.move(coords=p, offset=MOVE_OFFSET)
      res = strategy.rotate(res, angle=MOVE_ANGLE, inverse=False)
      res = strategy.rotate(res, angle=MOVE_ANGLE_INVERSE, inverse=True)
    results.append(res)
  return results


for label in strategies:
  wnd = GraphWin(label, WINDOW_WIDTH, WINDOW_HEIGHT)
  wnd.setBackground('yellow')
  strategy: clst.CalcStrategy = strategies[label]()
  pgram = Polygon(
    Point(X1, Y1),
    Point(X2, Y1),
    Point(X2 + X_OFFSET, Y2),
    Point(X1 + X_OFFSET, Y2)
  )
  draw_polygon(env=wnd, pol=pgram)

  for i in range(MOVE_TIMES):
    match strategy:
      case clst.ScalarStrategy():
        points = tuple((p.x, p.y) for p in pgram.points)
        results = points_mapper(points, strategy, offset=MOVE_OFFSET)
        pgram = Polygon([Point(x, y) for x, y in results])
      case clst.MatrixSequentialStrategy():
        points = tuple(np.array([p.x, p.y]) for p in pgram.points)
        results = points_mapper(points, strategy, offset=np.array(list(MOVE_OFFSET)))
        pgram = Polygon([Point(p[0], p[1]) for p in results])
      case clst.MatrixComposedStrategy():
        points = tuple(np.array([p.x, p.y, 1]) for p in pgram.points)
        offset_contaier = np.array([
          [1, 0, 0],
          [0, 1, 0],
          [MOVE_OFFSET[0], MOVE_OFFSET[1], 1]
        ])
        results = points_mapper(points, strategy, offset=offset_contaier)
        pgram = Polygon([Point(p[0], p[1]) for p in results])
    draw_polygon(env=wnd, pol=pgram)
  wnd.getMouse()
  wnd.close()
